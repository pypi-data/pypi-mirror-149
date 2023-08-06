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
    'version': '1.0.0',
    'description': 'sourcery-analytics is a library and command-line interface (CLI) for analyzing the code quality of Python packages, modules, or source code.',
    'long_description': '# Sourcery Analytics\n\n![PyPI](https://img.shields.io/pypi/v/sourcery-analytics)\n\n`sourcery-analytics` is a command line tool and library for statically analyzing Python code quality.\n\nGet started by installing using `pip`:\n\n```commandline\npip install sourcery-analytics\n```\n\nThis will install `sourcery-analytics` as a command-line tool.\nTo analyze a single Python file, use the `analyze` subcommand:\n\n```commandline\nsourcery-analytics analyze path/to/file.py\n```\n\nExample:\n\n```commandline\nsourcery-analytics analyze sourcery_analytics/analysis.py\n```\n\n```\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓\n┃ Method                                      ┃ length ┃ cyclomatic_complexity ┃ cognitive_complexity ┃ working_memory ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩\n│ sourcery_analytics.analysis.analyze         │      5 │                     1 │                    0 │              8 │\n│ sourcery_analytics.analysis.analyze_methods │      4 │                     1 │                    1 │             12 │\n└─────────────────────────────────────────────┴────────┴───────────────────────┴──────────────────────┴────────────────┘\n```\n\nAlternatively, import and run analysis using the library:\n\n```python\nfrom sourcery_analytics import analyze_methods\nsource = """\n    def cast_spell(self, spell):\n        if self.power < spell.power:\n            raise InsufficientPower\n        print(f"{self.name} cast {spell.name}!")\n"""\nanalyze_methods(source)\n# [{\'method_qualname\': \'.cast_spell\', \'method_length\': 3, \'method_cyclomatic_complexity\': 1, \'method_cognitive_complexity\': 1, \'method_working_memory\': 6}]\n```\n\nFor more, see the [docs](https://sourcery-analytics.sourcery.ai/).',
    'author': 'Ben Martineau',
    'author_email': 'ben@sourcery.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sourcery-ai/sourcery-analytics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
