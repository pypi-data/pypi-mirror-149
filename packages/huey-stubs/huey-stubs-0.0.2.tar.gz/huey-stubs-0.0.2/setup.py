# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huey-stubs']

package_data = \
{'': ['*'], 'huey-stubs': ['bin/*', 'contrib/*', 'contrib/djhuey/*']}

install_requires = \
['huey>=2.4.3,<3.0.0', 'typing-extensions>3.10.0,<5.0.0']

extras_require = \
{':python_version < "3.5"': ['typing>=3.10.0,<4.0.0']}

setup_kwargs = {
    'name': 'huey-stubs',
    'version': '0.0.2',
    'description': 'Type stubs for huey',
    'long_description': "# Type stubs for Huey\n[![PyPI version](https://badge.fury.io/py/huey-stubs.svg)](https://badge.fury.io/py/huey-stubs)\n\nThis package provides type stubs for the [huey](https://github.com/coleifer/huey) package.\n\nNote that the types aren't complete, though the most commonly used parts of the API should be covered.\nContributions to expand the coverage are welcome.\n\nIf you find incorrect annotations, please create an issue.\n\n## Installation\n\n```shell script\n$ pip install huey-stubs\n```\n",
    'author': 'Henrik Bruådal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/huey-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
