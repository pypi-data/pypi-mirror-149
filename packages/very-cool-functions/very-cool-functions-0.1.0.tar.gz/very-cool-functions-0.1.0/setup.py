# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['very_cool_functions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'very-cool-functions',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Magic Man',
    'author_email': 'zmartine0031@mymail.lausd.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
