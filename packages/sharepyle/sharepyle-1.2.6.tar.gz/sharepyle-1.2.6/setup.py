# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sharepyle']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bs4>=0.0.1,<0.0.2',
 'dateparser>=1.0.0,<2.0.0',
 'dpath>=2.0.1,<3.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'http-requester>=1.0.11,<2.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'sharepyle',
    'version': '1.2.6',
    'description': '',
    'long_description': None,
    'author': "Ryan O'Rourke",
    'author_email': 'ryan.orourke@welocalize.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
