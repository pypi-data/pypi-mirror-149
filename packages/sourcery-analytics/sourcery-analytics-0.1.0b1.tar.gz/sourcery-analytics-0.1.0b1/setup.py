# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sourcery_analytics', 'sourcery_analytics.cli', 'sourcery_analytics.metrics']

package_data = \
{'': ['*']}

install_requires = \
['astroid==2.11.2', 'more-itertools==8.12.0', 'rich==12.3.0', 'typer==0.4.1']

entry_points = \
{'console_scripts': ['sourcery-analytics = sourcery_analytics.main:app']}

setup_kwargs = {
    'name': 'sourcery-analytics',
    'version': '0.1.0b1',
    'description': 'sourcery-analytics is a library and command-line interface (CLI) for analyzing the code quality of Python packages, modules, or source code.',
    'long_description': None,
    'author': 'Ben',
    'author_email': 'ben@sourcery.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
