# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eues']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eues',
    'version': '0.1.1',
    'description': 'Einnahmeüberschussrechnung',
    'long_description': None,
    'author': 'Marco Heins',
    'author_email': 'ruttercrash@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
