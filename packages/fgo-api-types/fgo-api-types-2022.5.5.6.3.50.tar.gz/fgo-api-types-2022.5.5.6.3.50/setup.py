# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fgo_api_types']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3,<4', 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'fgo-api-types',
    'version': '2022.5.5.6.3.50',
    'description': 'Provide Pydantic types from FGO API',
    'long_description': None,
    'author': 'squaresmile',
    'author_email': 'squaresmile@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
