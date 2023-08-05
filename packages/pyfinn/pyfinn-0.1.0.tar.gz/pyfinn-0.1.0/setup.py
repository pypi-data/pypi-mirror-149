# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfinn']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent',
 'flask',
 'gunicorn',
 'redis',
 'requests-html',
 'urllib3>=1.24.2']

setup_kwargs = {
    'name': 'pyfinn',
    'version': '0.1.0',
    'description': 'Fetch real estate listing from finn.no and make available as JSON',
    'long_description': None,
    'author': 'Nikolai R Kristiansen',
    'author_email': 'nikolaik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
