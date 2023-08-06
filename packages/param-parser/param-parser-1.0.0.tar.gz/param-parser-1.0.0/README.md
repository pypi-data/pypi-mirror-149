param-parser
============

[![PyPI](https://badge.fury.io/py/param-parser.svg)](https://pypi.org/project/param-parser/)
[![Test Status](https://github.com/anexia/python-param-parser/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/anexia/python-param-parser/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/anexia/python-param-parser/branch/main/graph/badge.svg)](https://codecov.io/gh/anexia/python-param-parser)

`param-parser` is a parser library for a param string expression. Those expressions are arbitrary strings  with 
placeholders in it, where a placeholder consists of a name, an optional type and a list of options.

# Installation

With a [correctly configured](https://pipenv.pypa.io/en/latest/basics/#basic-usage-of-pipenv) `pipenv` toolchain:

```sh
pipenv install param-parser
```

You may also use classic `pip` to install the package:

```sh
pip install param-parser
```

# Getting started

Examples of param string expressions look as follows:

```
this-is-a-{param:string:option1,option2,option3}-expression
this-is-a-{param:string}-expression
this-is-a-{param}-expression
```

As you see, a param is introduced by an opening curly bracket, followed by the name of the param, a colon, the type of 
the param, another colon and a comma separated list of options. The param configuration gets terminated by a closing 
curly bracket. Note that the type and option configuration are optional, but the name is mandatory.

To parse an expression shown above, use the Python code as follows:

```python
import param_parser

result = param_parser.parse(r"this-is-a-{param:string:option1,option2,option3}-expression")

result[0]  # Gets a `param_parser.node.SequenceNode` instance
result[0].sequence_value  # Gets `"this-is-a-"` as a string

result[1]  # Gets a `param_parser.node.ParamNode` instance
result[1].param_name  # Gets `"param"` as a string
result[1].param_type  # Gets `"string"` as a string
result[1].param_options  # Gets `["option1", "option2", "option3"]` as a list of strings

result[2]  # Gets a `param_parser.node.SequenceNode` instance
result[2].sequence_value  # Gets `"-expression"` as a string
```

It is also possible to escape opening curly brackets, closing curly brackets, colons and commas as follows:

```python
import param_parser

result = param_parser.parse(r"this-is-a-\{param:string:option1,option2,option3\}-expression")

result[0]  # Gets a `param_parser.node.SequenceNode` instance
result[0].sequence_value  # Gets `"this-is-a-{param:string:option1,option2,option3}-expression"` as a string
```

# Supported versions

|             | Supported |
|-------------|-----------|
| Python 3.7  | ✓         |
| Python 3.8  | ✓         |
| Python 3.9  | ✓         |
| Python 3.10 | ✓         |
| Python 3.11 | ✓         |

# List of developers

* Andreas Stocker <AStocker@anexia-it.com>, Lead Developer
