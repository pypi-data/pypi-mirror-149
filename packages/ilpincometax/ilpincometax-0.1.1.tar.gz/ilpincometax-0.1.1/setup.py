# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ilpincometax']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ilpincometax',
    'version': '0.1.1',
    'description': 'library for calculating US federal tax for 2022, this is my personal project so do not recommend to use in production scenario with out testing',
    'long_description': None,
    'author': 'iluvpython',
    'author_email': 'iluvpython@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
