# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['framehaze']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'framehaze',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'wsuzume',
    'author_email': 'joshnobus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
