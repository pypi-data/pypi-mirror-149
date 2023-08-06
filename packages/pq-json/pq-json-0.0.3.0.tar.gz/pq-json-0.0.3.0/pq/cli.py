from .pq import Pipeline, _import_custom_modules
import sys, os
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="pq is a Python command-line JSON processor"
    )
    parser.add_argument("expression", nargs="?")
    parser.add_argument(
        "-c",
        "--module",
        help="Additional module from input string. Let's you define custom functions or other imports",
    )
    parser.add_argument(
        "-M",
        "--module-file",
        help="Additional modules from file. Let's you define custom functions",
    )

    if os.isatty(0):
        parser.print_help()
        return

    args = parser.parse_args()

    if args.module:
        _import_custom_modules(args.module)

    if args.module_file:
        _import_custom_modules(args.module_file, from_file=True)

    pipeline = Pipeline(json_stream=sys.stdin, str_input=args.expression)
    pipeline.run()
