# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyhold']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'keyhold',
    'version': '0.0.4',
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
