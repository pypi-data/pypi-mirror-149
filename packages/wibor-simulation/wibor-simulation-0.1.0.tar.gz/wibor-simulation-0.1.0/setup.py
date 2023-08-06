# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'wibor_simulation']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0']

extras_require = \
{'dev': ['pip>=20.3.1,<21.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'tox>=3.20.1,<4.0.0',
         'twine>=3.3.0,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-autorefs==0.1.1',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0'],
 'test': ['black==20.8b1',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'isort==5.6.4',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['wibor-simulation = wibor_simulation.cli:main']}

setup_kwargs = {
    'name': 'wibor-simulation',
    'version': '0.1.0',
    'description': 'Simulates the loan installments at different interest rates.',
    'long_description': '# wibor-simulation\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/wibor-simulation">\n    <img src="https://img.shields.io/pypi/v/wibor-simulation.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/PhillCli/wibor-simulation/actions">\n    <img src="https://github.com/PhillCli/wibor-simulation/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://wibor-simulation.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/wibor-simulation/badge/?version=latest" alt="Documentation Status">\n</a>\n\n<a href="https://pyup.io/repos/github/PhillCli/wibor-simulation/">\n<img src="https://pyup.io/repos/github/PhillCli/wibor-simulation/shield.svg" alt="Updates">\n</a>\n\n</p>\n\n\nSimulates the loan installments at different interest rates\n\n\n* Free software: MIT\n* Documentation: <https://wibor-simulation.readthedocs.io>\n\n\n## Features\n\n* simulations of loan installment based on changing interest rate (WIBOR6M)\n\n    ```shell\n    wibor-simulation simulation 100000.00 0.05 60 0.0025,0.0175,0.0270,0.0500,0.069\n    ```\n\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Filip Brzek',
    'author_email': 'filip.brzek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PhillCli/wibor-simulation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
