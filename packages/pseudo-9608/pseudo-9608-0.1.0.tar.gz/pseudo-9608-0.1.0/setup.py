# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pseudo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pseudo-9608',
    'version': '0.1.0',
    'description': 'An interpreter for 9608 pseudocode',
    'long_description': None,
    'author': 'JS Ng',
    'author_email': 'ngjunsiang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
