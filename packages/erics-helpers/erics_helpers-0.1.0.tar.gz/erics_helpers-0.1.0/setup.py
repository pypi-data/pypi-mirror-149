# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erics_helpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'erics-helpers',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ericcbonet',
    'author_email': 'ericcbonet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
