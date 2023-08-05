# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unsure']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ipykernel>=6.13.0,<7.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'unsure',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Vasanth Sarathy',
    'author_email': 'vsarathy@sift.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
