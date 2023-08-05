# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['milkjug']

package_data = \
{'': ['*']}

install_requires = \
['WebTest>=3.0.0,<4.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'parse>=1.19.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'milkjug',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
