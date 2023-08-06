# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antissrf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'antissrf',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jesus Aviles',
    'author_email': 'the.jesus.aviles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
