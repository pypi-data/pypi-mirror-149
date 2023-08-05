# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trove_classifiers_cli']

package_data = \
{'': ['*']}

install_requires = \
['trove-classifiers>=2022.4.30,<2023.0.0']

entry_points = \
{'console_scripts': ['trove-classifers = trove_classifers_cli.cli:main']}

setup_kwargs = {
    'name': 'trove-classifiers-cli',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/trove-classifers-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
