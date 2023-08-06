# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convert-string-to-number',
    'version': '0.1.3',
    'description': 'Convert string to number',
    'long_description': None,
    'author': 'NamTH',
    'author_email': 'namth2302@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
