# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['banquet']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0']

entry_points = \
{'console_scripts': ['banquet = banquet.bin:cli']}

setup_kwargs = {
    'name': 'banquet',
    'version': '0.0.1',
    'description': 'CLI tool for working with OpenAPI and Lambda functions',
    'long_description': '# Banquet\n\n> Development server for OpenAPI/Lambda Projects\n\n\n## Installing\n\nInstall and update using pip:\n\n`pip install -U banquet`\n',
    'author': 'Nick Snell',
    'author_email': 'nick.snell@manypets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/boughtbymany/banquet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
