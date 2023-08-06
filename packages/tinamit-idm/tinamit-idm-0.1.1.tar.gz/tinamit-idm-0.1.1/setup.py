# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinamit_idm']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'tinamit-idm',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'joelz575',
    'author_email': 'joel.harms@mail.mcgill.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
