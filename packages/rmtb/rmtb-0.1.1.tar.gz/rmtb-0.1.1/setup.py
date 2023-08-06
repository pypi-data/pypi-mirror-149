# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rmtb']

package_data = \
{'': ['*']}

install_requires = \
['rel>=0.4.7,<0.5.0', 'websocket-client>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'rmtb',
    'version': '0.1.1',
    'description': 'A simple library for making rmtb bots in python.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
