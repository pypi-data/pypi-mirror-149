# Basic Iterator Operators for Python

This package provides basic functions on sequences (now only `list` is supported).
All these provided functions are defined in functional way and do not update given arguments, but return newly constructed values.


## Install

```sh
$ pip install basic_iter
```

## Develop

## Install dependencies for developing

```sh
basic_iter$ poetry install --no-root
```


### Generate documents

To generate documents:

```sh
basic_iter$ make doc
```

This will generate documentation under `./docs/build/html`.


## Format Checking

For format checking by black:

```sh
basic_iter$ make format_check
```


## Type Checking

For type checking by mypy:

```sh
basic_iter$ make type_check
```


## Unit Test

For executing unit tests:

```sh
basic_iter$ make test
```


