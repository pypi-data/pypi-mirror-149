# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chess_server']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0', 'chess>=1.9.0,<2.0.0', 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'chess-server',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tilak Patel',
    'author_email': 'ptilak142@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
