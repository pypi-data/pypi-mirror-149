# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polygon', 'polygon.rest', 'polygon.rest.models']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'polygon-api-client',
    'version': '1.0.0b6',
    'description': 'Official Polygon.io REST and Websocket client.',
    'long_description': None,
    'author': 'polygon.io',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://polygon.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
