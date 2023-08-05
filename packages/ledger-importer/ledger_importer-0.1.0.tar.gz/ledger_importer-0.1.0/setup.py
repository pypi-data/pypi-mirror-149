# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ledger_importer']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'ledger-importer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Florent Espanet',
    'author_email': 'florent.esp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
