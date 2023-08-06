# pq-json
pq is a Python command-line JSON processor - **almost** like (atleast inspired by 🐶️) [jq](https://github.com/stedolan/jq), but using Python focusing on simplicity and convenience with familiar syntax.

## Install
```
pip install pq-json
```


Here is a simple example for parsing JSON. Output from pq is pretty printed using [Rich](https://github.com/Textualize/rich).
```
$ echo '{"text": "Text here", "header": "Header", "list": [1,2,3]}' | pq
```
```json
{
  "text": "Text here",
  "header": "Header",
  "list": [
    1,
    2,
    3
  ]
}
```
![Pretty Parse](https://github.com/mumubebe/pq/blob/main/images/prettyrprint.png)

### Filters
The processing is handled with filters, like in jq.
j represents the current input object in a filter. 
```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
```
```json
"data"
```

```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j['example']"
```
```json
"data"
```

As default, None will not be passed.
```
$ echo '{"example": "data", "nothing": "interesting"}' | pq "j.get('nada')"

```

### List slicing

JSON arrays are converted to Python list. 
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[0]"
```
```json
{
  "name": "eric",
  "age": 22
}
```
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[-1]"
```
```json
{
  "name": "daniel",
  "age": 44
}
```

An array always iterates to the next filter. Here we are using the slice symbol [:] to highlight that we are working with an array. 
```
$ echo '[{"name": "eric", "age": 22}, {"name": "daniel", "age": 44}]' | pq "j[:]"
```

```json
{
  "name": "eric",
  "age": 22
}
{
  "name": "daniel",
  "age": 44
}
```

Want to send the full array to the next filter? Wrap array around ```[]``` brackets like:
```
$ echo '[1,2,3,4,5]' | pq "[j[:]]"
```
```json
[
  1,
  2,
  3,
  4,
  5
]
```


### Pipes
Pipes let you chain multiple filters by produce output to the filter to the right of the pipe. Under the hood a pipeline is a chain of generators. An array will for example yield multiple elements to the right. 

input: 
```json
["a", "b", "c", "d"]
```
```
pq "j[0:2] | j.upper()"
      |         |
   filter1   filter2

produces the following result:
"A"
"B"

In this case, the expression j.upper() will be run each time.

j[0] -> "a".upper() -> "A"
j[1] -> "b".upper() -> "B"

Another example:

$ echo '[1,2,3,4,5,6,7,8,9]' | pq 'j[:] | j**2+50'
```
```json
51
54
59
66
75
86
99
114
131
```
### Array constructs
Above example outputs a list of integers. It's possible to wrap it all into a single array by using [] around the full expression.
```
$ echo '[1,2,3,4,5,6,7,8,9]' | pq '[j[:] | j**2+50]'
```
```json
[51, 54, 59, 66, 75, 86, 99, 114, 131]
```
### Object constructs
```
$ echo '{"name":"jan", "age":4, "parents": ["lisa", "dan"]}' | pq '{"name": j["name"], "parents": j["parents"]}'
```
```json
{
  "name": "jan",
  "parents": [
    "lisa",
    "dan"
  ]
}
```

### Other examples

We can easily use built-in functions in Python
```
$ echo "[1,2,3,4,5,6]" | pq 'sum(j) | {"total": j}'
```
```json
{
  "total": 21
}
```
