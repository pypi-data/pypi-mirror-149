# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pya2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pya2',
    'version': '0.0.1',
    'description': 'Python Ann Arbor',
    'long_description': None,
    'author': 'Elijah Wilson',
    'author_email': 'dev.tizz98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
