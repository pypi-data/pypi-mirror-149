# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['securecookies']

package_data = \
{'': ['*']}

install_requires = \
['cryptograpy>=0.0.0,<0.0.1', 'starlette>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'starlette-securecookies',
    'version': '1.0.0',
    'description': 'Secure cookie middleware for Starlette applications.',
    'long_description': None,
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thearchitector/starlette-securecookies',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
