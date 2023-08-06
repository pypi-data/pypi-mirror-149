# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_huey-stubs']

package_data = \
{'': ['*'], 'django_huey-stubs': ['management/*', 'management/commands/*']}

install_requires = \
['django-huey>=1.0.0,<2.0.0',
 'huey-stubs>=0.0.1,<0.0.2',
 'typing-extensions>3.10.0,<5.0.0']

setup_kwargs = {
    'name': 'django-huey-stubs',
    'version': '0.0.1',
    'description': 'Type stubs for django-huey',
    'long_description': '# Type stubs for django-huey\n[![PyPI version](https://badge.fury.io/py/django-huey-stubs.svg)](https://badge.fury.io/py/django-huey-stubs)\n\nThis package provides type stubs for the [django-huey](https://github.com/coleifer/django-huey) package.\n\nIf you find incorrect annotations, please create an issue.  \n\n## Installation\n\n```shell script\n$ pip install django-huey-stubs\n```\n',
    'author': 'Henrik Bruådal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/django-huey-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
