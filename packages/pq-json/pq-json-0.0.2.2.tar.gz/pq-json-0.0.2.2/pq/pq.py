from pq.utils import *
from rich import print_json
import json

class Filter:
    def __init__(self, expr, producer, first=False):
        self.first = first
        self.producer = producer
        self.expr = expr
        if not first:
            self._compiled = self._compile()

    def _compile(self):
        return compile(f"({self.expr})", "<string>", "eval")

    def evaluate(self, item):
        return eval(self._compiled, {"j": item}, globals())

    def eval_loop(self):
        if self.first:
            yield self.producer
        else:
            for p in self.producer.eval_loop():
                if not p:
                    continue
                val = self.evaluate(p)
                if not val:
                    continue

                # Always iterate if list
                elif type(val) == list:
                    for l in val:
                        yield l
                else:
                    yield val


class Pipeline:
    """One or multiple filters connected"""

    def __init__(self, json_stream, str_input):
        str_input = str_input or ""

        jsondata = json.loads(json_stream.read())

        # Array constructs around expression
        if len(str_input) and (str_input[0] == "[" and str_input[-1] == "]"):
            str_input = str_input[1:-1]
            self.array = True
        else:
            self.array = False

        pipe_filters = [s.strip() for s in str_input.split("|")]

        self.filters = self._build_pipeline(jsondata, pipe_filters)

    @property
    def last(self):
        """Returns last filter in pipeline"""
        if len(self.filters):
            return self.filters[-1]
        else:
            raise IndexError("No filters in pipeline")

    @property
    def first(self):
        """Returns first user declared filters in pipeline"""
        if len(self.filters):
            return self.filters[1]
        else:
            raise IndexError("No filters in pipeline")

    def _build_pipeline(self, input_data, pipe_expression):
        """Build a pipeline from user input pipeline-string

        A pipeline consist of atleast "input | output" even if users has not defined any filters, where filters
        are between input and output.

        Example of user defined filters:
        $ pq "j[:] | j['name']"
        --->
        The right right filter consumes what the left filter j[:] yields.

        Under the hood, with input and output attached:
        (input data) | j[:] | j['name'] | -> (output)
        """
        filters = []
        for e in pipe_expression:
            if not filters:
                # input data, not a filter per se
                filters.append(Filter(e, producer=input_data, first=True))
            if e:
                filters.append(Filter(e, producer=filters[-1]))
        return filters

    def run(self):
        """Run pipeline chain and print ouput"""

        # Buff yielded items if array filter
        if self.array:
            buff = []
            for output in self.last.eval_loop():
                buff.append(output)

            self.print(buff)
        else:
            for output in self.last.eval_loop():
                self.print(output)

    def print(self, output):
        try:
            print_json(json.dumps(output))
        except:
            print(json.dumps(output, indent=2))


def _import_global(import_str):
    """Import modules to global context"""
    exec(import_str, globals())
