# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'wxy121517761848']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'pandas>1.1.1',
 'requests>2.27.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0',
 'types-requests>2.27.0',
 'types-tabulate>=0.8.8,<0.9.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'tox-conda>=0.8.2,<0.9.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-material>=8.1.0,<9.0.0',
         'mkdocstrings>=0.16.0,<0.17.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0',
         'mkdocs-include-markdown-plugin>=2.8.0,<3.0.0',
         'mkdocs-git-revision-date-plugin>=0.3.1,<0.4.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.900,<0.901',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'wxy121517761848',
    'version': '0.0.10',
    'description': 'Some lite description.',
    'long_description': '# wxy121517761848\n\n\n[![pypi](https://img.shields.io/pypi/v/wxy121517761848.svg)](https://pypi.org/project/wxy121517761848/)\n[![python](https://img.shields.io/pypi/pyversions/wxy121517761848.svg)](https://pypi.org/project/wxy121517761848/)\n[![Build Status](https://github.com/nazq/wxy121517761848/actions/workflows/dev.yml/badge.svg)](https://github.com/nazq/wxy121517761848/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/nazq/wxy121517761848/branch/main/graphs/badge.svg)](https://codecov.io/github/nazq/wxy121517761848)\n\n\n\nSome lite description\n\n\n* Documentation: <https://nazq.github.io/wxy121517761848>\n* GitHub: <https://github.com/nazq/wxy121517761848>\n* PyPI: <https://pypi.org/project/wxy121517761848/>\n* Free software: Apache-2.0\n\n\n## Features\n\n* TODO\n\n\n',
    'author': 'Anon',
    'author_email': 'naz.quadri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nazq/wxy121517761848',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
