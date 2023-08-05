# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysparker']

package_data = \
{'': ['*']}

install_requires = \
['datacompy>=0.8.1', 'loguru>=0.6.0']

setup_kwargs = {
    'name': 'pysparker',
    'version': '0.1.1',
    'description': 'Some utility functions for PySpark.',
    'long_description': None,
    'author': 'Ben Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
