# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinytorchtest']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'tinytorchtest',
    'version': '0.7.0',
    'description': 'A tiny test suite for pytorch based machine learning models.',
    'long_description': None,
    'author': 'Alex',
    'author_email': 'adrysdale@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
