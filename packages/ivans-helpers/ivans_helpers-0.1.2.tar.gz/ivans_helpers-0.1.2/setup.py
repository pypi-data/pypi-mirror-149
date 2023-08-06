# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ivans_helpers', 'ivans_helpers.ivans_helpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ivans-helpers',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Ivan Thung',
    'author_email': 'ivanthung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ivanthung/ivan_helpers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
