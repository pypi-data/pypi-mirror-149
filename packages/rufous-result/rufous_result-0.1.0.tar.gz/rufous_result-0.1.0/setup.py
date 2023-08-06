# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rufous_result']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rufous-result',
    'version': '0.1.0',
    'description': "Translation of Rust's Result type to Python 3.",
    'long_description': None,
    'author': 'Gavriel Rachael-Homann',
    'author_email': 'gavriel@gavriel.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
