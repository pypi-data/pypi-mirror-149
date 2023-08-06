# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basic_iter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'basic-iter',
    'version': '0.0.4',
    'description': 'A basic set of functions on iterators',
    'long_description': '# Basic Iterator Operators for Python\n\nThis package provides basic functions on sequences (now only `list` is supported).\nAll these provided functions are defined in functional way and do not update given arguments, but return newly constructed values.\n\n\n## Install\n\n```sh\n$ pip install basic_iter\n```\n\n## Develop\n\n## Install dependencies for developing\n\n```sh\nbasic_iter$ poetry install --no-root\n```\n\n\n### Generate documents\n\nTo generate documents:\n\n```sh\nbasic_iter$ make doc\n```\n\nThis will generate documentation under `./docs/build/html`.\n\n\n## Format Checking\n\nFor format checking by black:\n\n```sh\nbasic_iter$ make format_check\n```\n\n\n## Type Checking\n\nFor type checking by mypy:\n\n```sh\nbasic_iter$ make type_check\n```\n\n\n## Unit Test\n\nFor executing unit tests:\n\n```sh\nbasic_iter$ make test\n```\n\n\n',
    'author': 'Takayuki Goto',
    'author_email': 'nephits@gmail.com',
    'maintainer': 'Takayuki Goto',
    'maintainer_email': 'nephits@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
