# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['secstache']
install_requires = \
['argparse>=1.4.0,<2.0.0', 'boto3>=1.21.37,<2.0.0', 'pystache>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['secstache = secstache:main']}

setup_kwargs = {
    'name': 'secstache',
    'version': '0.3.6',
    'description': '',
    'long_description': None,
    'author': 'Shinichi Urano',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
