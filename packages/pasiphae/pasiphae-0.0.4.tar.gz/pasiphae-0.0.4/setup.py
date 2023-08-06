# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pasiphae']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.10b0,<22.0',
 'click>=8.0.3,<9.0.0',
 'graphql-core>=3.1.6,<4.0.0',
 'isort>=5.10.0,<6.0.0']

entry_points = \
{'console_scripts': ['pasiphae = pasiphae.cli:pasiphae']}

setup_kwargs = {
    'name': 'pasiphae',
    'version': '0.0.4',
    'description': 'Generate and update ariadne service from graphql schema',
    'long_description': '========\nPasiphaë\n========\n\n\n.. image:: https://img.shields.io/pypi/v/pasiphae.svg\n        :target: https://pypi.python.org/pypi/pasiphae\n\n.. image:: https://github.com/dswistowski/pasiphae/actions/workflows/tests.yml/badge.svg\n        :target: https://github.com/dswistowski/pasiphae/actions/workflows/tests.yml\n\n.. image:: https://readthedocs.org/projects/pasiphae/badge/?version=latest\n        :target: https://pasiphae.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nPasiphaë will generate Ariadne service from provided graphql schema\n\n* Free software: MIT license\n* Documentation: https://pasiphae.readthedocs.io.\n\n\nFeatures\n--------\n\n* TBD\n',
    'author': 'Damian Świstowski',
    'author_email': 'damian@swistowski.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dswistowski/pasiphae/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
