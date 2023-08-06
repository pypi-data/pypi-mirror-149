# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_uzi', 'sanic_uzi.ext']

package_data = \
{'': ['*']}

install_requires = \
['sanic[ext]>=22.3.1,<23.0.0',
 'typing-extensions>=4.1.1,<5.0.0',
 'uzi>=0.0.0,<0.1.0']

setup_kwargs = {
    'name': 'sanic-uzi',
    'version': '0.0.0',
    'description': 'Sanic uzi adapter',
    'long_description': '# Sanic Uzi\n\n\n[![PyPi version][pypi-image]][pypi-link]\n[![Supported Python versions][pyversions-image]][pyversions-link]\n[![Build status][ci-image]][ci-link]\n[![Coverage status][codecov-image]][codecov-link]\n\n\n`Uzi` is a [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) library for Python.\n\n\n\n## Installation\n\nInstall from [PyPi](https://pypi.org/project/sanic-uzi/)\n\n```\npip install sanic-uzi\n```\n\n## Documentation\n\nFull documentation is available [here][docs-link].\n\n\n\n## Production\n\n__This package is still in active development and should not be used in production environment__\n\n\n\n\n[docs-link]: https://pyuzi.github.io/sanic-uzi/\n[pypi-image]: https://img.shields.io/pypi/v/sanic-uzi.svg?color=%233d85c6\n[pypi-link]: https://pypi.python.org/pypi/sanic-uzi\n[pyversions-image]: https://img.shields.io/pypi/pyversions/sanic-uzi.svg\n[pyversions-link]: https://pypi.python.org/pypi/sanic-uzi\n[ci-image]: https://github.com/pyuzi/sanic-uzi/actions/workflows/workflow.yaml/badge.svg?event=push&branch=master\n[ci-link]: https://github.com/pyuzi/sanic-uzi/actions?query=workflow%3ACI%2FCD+event%3Apush+branch%3Amaster\n[codecov-image]: https://codecov.io/gh/pyuzi/sanic-uzi/branch/master/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/pyuzi/sanic-uzi\n\n',
    'author': 'David Kyalo',
    'author_email': 'davidmkyalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyuzi/sanic-uzi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
