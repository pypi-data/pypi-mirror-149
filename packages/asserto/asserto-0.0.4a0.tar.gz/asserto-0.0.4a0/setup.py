# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asserto']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.3.0,<13.0.0']

setup_kwargs = {
    'name': 'asserto',
    'version': '0.0.4a0',
    'description': 'A fluent DSL for python assertions.',
    'long_description': '![Asserto](.github/images/logo.png)\n\n![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)\n[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)\n[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)\n\n## Asserto:\n\nAsserto is a clean, fluent and powerful assertion library for python.  We recommend using `pytest` as a test\nrunner but asserto will work well with any test runner.\n\n>Asserto was developed using pytest as it\'s test runner and has a `pytest-asserto` plugin that exposes asserto\n>through a fixture.  Asserto will work on any runner or even without one.  Note: It is common practice for a\n>test runner to apply assertion rewriting to change the behaviour of the `assert` keyword under the hood.\n\nThe main features of asserto are (and will be):\n\n+ Chainable and Fluent API.\n+ Ability for both `Hard` and `Soft` assertions.\n+ Rich diffs to highlight problems, reduce churn and improve effeciency and debuggability.\n+ Dynamic assertions; check any obj attribute or invoke any of it\'s function types.\n+ Robust set of methods out of the box for common types.\n+ Extensibility.  Bolt on your own assetions at runtime.\n+ Human error detection, elaborate warnings when something is amiss.\n+ Much more to come.\n\n## Usage:\n\n```python\nfrom asserto import asserto\n\ndef test_foo() -> None:\n    asserto("Hello").has_length(5).matches(r"\\w{5}$").ends_with("lo").starts_with("Hel")\n```\n\nIf you use pytest; a fixture is available for an `Asserto` factory function:\n\n```python\ndef test_bar(asserto) -> None:  # No imports; just use the fixture.\n    asserto("Hello").has_length(5).matches(r"\\w{4}$").ends_with("lo").starts_with("Hel")\n```\n\nIf you want to check many assertions in a single test without failing until after all:\n\n```python\ndef test_baz(asserto) -> None:\n    with asserto("Baz") as context:\n        # asserto when used in a python context is run in \'soft\' mode;\n        # upon exiting the context; congregated errors are subsequently raised (if any)\n        context.starts_with("B")\n        context.ends_with("z")\n        context.is_equal_to("Baz")\n        context.is_length(2)  # Uh oh a failure!\n```\n\nResults in:\n\n```shell\n    def test_foo(asserto) -> None:\n>       with asserto("Bar") as context:\nE       AssertionError: 1 Soft Assertion Failures\nE       [AssertionError("Length of: \'Bar\' was not equal to: 2")]\n```\n',
    'author': 'symonk',
    'author_email': 'jackofspaces@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
