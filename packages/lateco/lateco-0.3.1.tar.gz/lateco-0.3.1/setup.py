# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lateco']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.16.3,<8.0.0', 'pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'lateco',
    'version': '0.3.1',
    'description': 'A framework for creating, managing and analysing large text corpora',
    'long_description': None,
    'author': 'Thomas Zastrow',
    'author_email': 'post@thomas-zastrow.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
