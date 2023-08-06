# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_gdrive']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'google-api-python-client>=2.47.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.1,<0.6.0',
 'loguru>=0.6.0,<0.7.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'simple-gdrive',
    'version': '1.0.0',
    'description': 'Simple command to help download and upload big files to Google Drive (using their official Drive APIs)',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
