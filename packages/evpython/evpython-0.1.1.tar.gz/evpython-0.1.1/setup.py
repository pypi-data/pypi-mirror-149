# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evpython']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.14.1,<4.0.0', 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'evpython',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Henrique Cunha',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
