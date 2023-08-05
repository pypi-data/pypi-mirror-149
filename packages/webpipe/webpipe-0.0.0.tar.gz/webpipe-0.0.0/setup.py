# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpipe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'webpipe',
    'version': '0.0.0',
    'description': 'webpipe',
    'long_description': None,
    'author': 'Nikhil Rao',
    'author_email': 'nikhil@webpipe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
