# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['om_helper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'om-helper',
    'version': '0.0.16',
    'description': 'om`s helper',
    'long_description': None,
    'author': 'iulmt',
    'author_email': '1817556010@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
