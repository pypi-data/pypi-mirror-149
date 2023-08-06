# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitignore_cli_tddschn']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gitignore = gitignore_cli_tddschn.cli:main']}

setup_kwargs = {
    'name': 'gitignore-cli-tddschn',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/gitignore-cli-tddschn',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
