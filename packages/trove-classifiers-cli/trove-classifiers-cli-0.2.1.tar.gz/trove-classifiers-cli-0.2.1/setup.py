# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trove_classifiers_cli']

package_data = \
{'': ['*']}

install_requires = \
['trove-classifiers>=2022.4.30,<2023.0.0']

entry_points = \
{'console_scripts': ['trove-classifiers = trove_classifiers_cli.cli:main']}

setup_kwargs = {
    'name': 'trove-classifiers-cli',
    'version': '0.2.1',
    'description': '',
    'long_description': '# Trove Classifiers CLI\n\nCLI for PyPI Trove Classifiers\n\n- [Trove Classifiers CLI](#trove-classifiers-cli)\n\t- [Usage](#usage)\n\t- [Examples](#examples)\n\t\t- [Basic usage](#basic-usage)\n\t\t- [--tree](#--tree)\n\t\t- [--quoted-list](#--quoted-list)\n## Usage\n\n```\n$ trove-classifiers --help\nusage: trove-classifiers [-h] [-I] [-q] [-t] [MATCH ...]\n\nCLI for PyPI Trove Classifiers\n\npositional arguments:\n  MATCH              String(s) to search for (default: [None])\n\noptions:\n  -h, --help         show this help message and exit\n  -I, --case         Perform case sensitive matching. (default: False)\n  -q, --quoted-list  Output a quoted list (default: False)\n  -t, --tree         Format output as a tree (default: False)\n```\n\n## Examples\n\n### Basic usage\n```\n$ trove-classifiers macos\nEnvironment :: MacOS X\nEnvironment :: MacOS X :: Aqua\nEnvironment :: MacOS X :: Carbon\nEnvironment :: MacOS X :: Cocoa\nOperating System :: MacOS\nOperating System :: MacOS :: MacOS 9\nOperating System :: MacOS :: MacOS X\n```\n\n### --tree\n```\n$ trove-classifiers macos -t\nEnvironment :: MacOS X\n        Environment :: MacOS X :: Aqua\n        Environment :: MacOS X :: Carbon\n        Environment :: MacOS X :: Cocoa\nOperating System :: MacOS\n        Operating System :: MacOS :: MacOS 9\n        Operating System :: MacOS :: MacOS X\n```\n\n### --quoted-list\n```\n$ trove-classifiers macos -q\n"Environment :: MacOS X",\n"Environment :: MacOS X :: Aqua",\n"Environment :: MacOS X :: Carbon",\n"Environment :: MacOS X :: Cocoa",\n"Operating System :: MacOS",\n"Operating System :: MacOS :: MacOS 9",\n"Operating System :: MacOS :: MacOS X",\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/trove-classifiers-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
