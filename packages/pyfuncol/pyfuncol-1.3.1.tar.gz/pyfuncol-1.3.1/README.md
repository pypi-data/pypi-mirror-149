# pyfuncol

![CI](https://github.com/didactic-meme/pyfuncol/actions/workflows/python-app.yml/badge.svg)
[![codecov](https://codecov.io/gh/didactic-meme/pyfuncol/branch/main/graph/badge.svg)](https://codecov.io/gh/didactic-meme/pyfuncol)
![PyPI](https://img.shields.io/pypi/v/pyfuncol?color=blue)
[![Downloads](https://pepy.tech/badge/pyfuncol)](https://pepy.tech/project/pyfuncol)
[![Documentation Status](https://readthedocs.org/projects/pyfuncol/badge/?version=latest)](https://pyfuncol.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/didactic-meme/pyfuncol)](https://github.com/didactic-meme/pyfuncol/blob/main/LICENSE)

- [pyfuncol](#pyfuncol)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Usage without forbiddenfruit](#usage-without-forbiddenfruit)
    - [API](#api)
  - [Documentation](#documentation)
  - [Compatibility](#compatibility)
  - [Contributing](#contributing)
  - [License](#license)

A Python functional collections library. It _extends_ collections built-in types with useful methods to write functional Python code. It uses [Forbidden Fruit](https://github.com/clarete/forbiddenfruit) under the hood.

pyfuncol provides:

- Standard "eager" methods, such as `map`, `flat_map`, `group_by`, etc.
- Parallel methods, such as `par_map`, `par_flat_map`, etc.
- Pure methods that leverage memoization to improve performance, such as `pure_map`, `pure_flat_map`, etc.
- Lazy methods that return iterators and never materialize results, such as `lazy_map`, `lazy_flat_map`, etc.

pyfuncol can also be [used without forbiddenfruit](#usage-without-forbiddenfruit).

## Installation

`pip install pyfuncol`

## Usage

> **Note:** If you are not using forbiddenfruit, the functions will not extend the builtins. Please [see here](#usage-without-forbiddenfruit) for usage without forbiddenfruit.

To use the methods, you just need to import pyfuncol. Some examples:

```python
import pyfuncol

[1, 2, 3, 4].map(lambda x: x * 2).filter(lambda x: x > 4)
# [6, 8]

[1, 2, 3, 4].fold_left(0, lambda acc, n: acc + n)
# 10

{1, 2, 3, 4}.map(lambda x: x * 2).filter_not(lambda x: x <= 4)
# {6, 8}

["abc", "def", "e"].group_by(lambda s: len(s))
# {3: ["abc", "def"], 1: ["e"]}

{"a": 1, "b": 2, "c": 3}.flat_map(lambda kv: {kv[0]: kv[1] ** 2})
# {"a": 1, "b": 4, "c": 9}
```

pyfuncol provides parallel operations (for now `par_map`, `par_flat_map`, `par_filter` and `par_filter_not`):

```python
[1, 2, 3, 4].par_map(lambda x: x * 2).par_filter(lambda x: x > 4)
# [6, 8]

{1, 2, 3, 4}.par_map(lambda x: x * 2).par_filter_not(lambda x: x <= 4)
# {6, 8}

{"a": 1, "b": 2, "c": 3}.par_flat_map(lambda kv: {kv[0]: kv[1] ** 2})
# {"a": 1, "b": 4, "c": 9}
```

pyfuncol provides operations leveraging memoization to improve performance (for now `pure_map`, `pure_flat_map`, `pure_filter` and `pure_filter_not`). These versions work only for **pure** functions (i.e., all calls to the same args return the same value) on hashable inputs:

```python
[1, 2, 3, 4].pure_map(lambda x: x * 2).pure_filter(lambda x: x > 4)
# [6, 8]

{1, 2, 3, 4}.pure_map(lambda x: x * 2).pure_filter_not(lambda x: x <= 4)
# {6, 8}

{"a": 1, "b": 2, "c": 3}.pure_flat_map(lambda kv: {kv[0]: kv[1] ** 2})
# {"a": 1, "b": 4, "c": 9}
```

pyfuncol provides lazy operations that never materialize results:

```python
list([1, 2, 3, 4].lazy_map(lambda x: x * 2).lazy_filter(lambda x: x > 4))
# [6, 8]

list({1, 2, 3, 4}.lazy_map(lambda x: x * 2).lazy_filter_not(lambda x: x <= 4))
# [6, 8]

list({"a": 1, "b": 2, "c": 3}.lazy_flat_map(lambda kv: {kv[0]: kv[1] ** 2}))
# [("a", 1), ("b", 4), ("c", 9)]

set([1, 2, 3, 4].lazy_map(lambda x: x * 2).lazy_filter(lambda x: x > 4))
# {6, 8}
```

### Usage without forbiddenfruit

If you are using a Python interpreter other than CPython, forbiddenfruit will not work.

Fortunately, if forbiddenfruit does not work on your installation or if you do not want to use it, pyfuncol also supports direct function calls without extending builtins.

```python
from pyfuncol import list as pfclist

pfclist.map([1, 2, 3], lambda x: x * 2)
# [2, 4, 6]
```

### API

For lists, please refer to the [docs](https://pyfuncol.readthedocs.io/en/latest/pyfuncol.html#module-pyfuncol.list).

For dictionaries, please refer to the [docs](https://pyfuncol.readthedocs.io/en/latest/pyfuncol.html#module-pyfuncol.dict).

For sets and frozensets, please refer to the [docs](https://pyfuncol.readthedocs.io/en/latest/pyfuncol.html#module-pyfuncol.set).

For more details, please have a look at the [API reference](https://pyfuncol.readthedocs.io/en/latest/modules.html).

We support all subclasses with default constructors (`OrderedDict`, for example).

## Documentation

See <https://pyfuncol.readthedocs.io/>.

## Compatibility

For functions to extend built-ins, [Forbidden Fruit](https://github.com/clarete/forbiddenfruit) is necessary (CPython only).

## Contributing

See the [contributing guide](https://github.com/didactic-meme/pyfuncol/blob/main/CONTRIBUTING.md) for detailed instructions on how to get started with the project.

## License

pyfuncol is licensed under the [MIT license](https://github.com/didactic-meme/pyfuncol/blob/main/LICENSE).
