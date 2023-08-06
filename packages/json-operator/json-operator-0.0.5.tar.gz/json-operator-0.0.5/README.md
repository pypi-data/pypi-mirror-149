 json-operator is a tool which provides operations on JSON data.

If a JSON object is regarded as a data set (key-value pair), we can apply set operations on it. An example is to find out all the common attributes in two JSON objects.
Another example is to check if two JSON objects are equal or not.

Currently json-operator supports 4 operations: equal, intersection, union, subtract.

<!-- more -->

# Installation

```commandline
$ pip install json-operator
```

# Embedded examples

json-operator can be embedded into your program as a library.

```examples
import json_operator as jo
import json

# construct JSON objects
obj1 = json.loads('{"a": 1, "b":2}')
obj2 = json.loads('{"a": 1, "c":"3"}')

# equal operation
res = jo.equal(obj1, obj2)           # False

# intersection
res = jo.intersection(obj1, obj2)    # {"a":1}

# union
res = jo.union(obj1, obj2)           # {"a":1, "b":2, "c":"3"}

# subtract
res = jo.subtract(obj1, obj2)        # {"b":2}

res = jo.subtract(obj2, obj1)        # {"c":"3"}
```

# Standalone usage

```commandline
$ json-operator --help

usage: json-operator [--lt LT] [--rt RT] [--lf LF] [--rf RF] [--out OUT] [--help] [operator]

command utility to operate on JSON objects. Supported operators: equal, intersection, subtract, union.

positional arguments:
  operator   action command

optional arguments:
  --lt LT    left-side JSON text. Overwrite --lf option
  --rt RT    right-side JSON text. Overwrite --rf option
  --lf LF    left-side file where JSON is stored
  --rf RF    right-side file where JSON is stored
  --out OUT  output file. Default is stdout
  --help     print this help message
```

