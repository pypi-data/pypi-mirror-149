# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycontexts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycontexts',
    'version': '0.1.4',
    'description': '',
    'long_description': 'None',
    'author': 'jack',
    'author_email': 'jack@gallabytes.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
