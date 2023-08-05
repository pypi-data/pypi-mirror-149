# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cardano_helpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cardano-helpers',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Samuel Ostholm',
    'author_email': 'kalltrum@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
