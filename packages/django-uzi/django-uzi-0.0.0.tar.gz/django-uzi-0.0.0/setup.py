# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_uzi']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.4,<5.0.0', 'typing-extensions>=4.1.1,<5.0.0', 'uzi>=0.0.0,<0.1.0']

setup_kwargs = {
    'name': 'django-uzi',
    'version': '0.0.0',
    'description': 'uzi dependency injection adapter for django',
    'long_description': '# Django Uzi\n\n\n[![PyPi version][pypi-image]][pypi-link]\n[![Supported Python versions][pyversions-image]][pyversions-link]\n[![Build status][ci-image]][ci-link]\n[![Coverage status][codecov-image]][codecov-link]\n\n\n`Uzi` is a [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) library for Python.\n\n\n\n## Installation\n\nInstall from [PyPi](https://pypi.org/project/django-uzi/)\n\n```\npip install django-uzi\n```\n\n## Documentation\n\nFull documentation is available [here][docs-link].\n\n\n\n## Production\n\n__This package is still in active development and should not be used in production environment__\n\n\n\n\n[docs-link]: https://pyuzi.github.io/django-uzi/\n[pypi-image]: https://img.shields.io/pypi/v/django-uzi.svg?color=%233d85c6\n[pypi-link]: https://pypi.python.org/pypi/django-uzi\n[pyversions-image]: https://img.shields.io/pypi/pyversions/django-uzi.svg\n[pyversions-link]: https://pypi.python.org/pypi/django-uzi\n[ci-image]: https://github.com/pyuzi/django-uzi/actions/workflows/workflow.yaml/badge.svg?event=push&branch=master\n[ci-link]: https://github.com/pyuzi/django-uzi/actions?query=workflow%3ACI%2FCD+event%3Apush+branch%3Amaster\n[codecov-image]: https://codecov.io/gh/pyuzi/django-uzi/branch/master/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/pyuzi/django-uzi\n\n',
    'author': 'David Kyalo',
    'author_email': 'davidmkyalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyuzi/django-uzi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
