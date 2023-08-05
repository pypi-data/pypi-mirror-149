# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dp2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dp2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Drozdov',
    'author_email': 'andrew@mrdrozdov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
