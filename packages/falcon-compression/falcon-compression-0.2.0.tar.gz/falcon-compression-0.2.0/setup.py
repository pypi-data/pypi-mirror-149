# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['falcon_compression']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0']

setup_kwargs = {
    'name': 'falcon-compression',
    'version': '0.2.0',
    'description': 'Compression middleware for Falcon',
    'long_description': '\n# Falcon Compression Middleware\n\nMiddleware to apply content compression to Falcon responses.\n',
    'author': 'Will Newton',
    'author_email': 'will.newton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willnewton/falcon-compression',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
