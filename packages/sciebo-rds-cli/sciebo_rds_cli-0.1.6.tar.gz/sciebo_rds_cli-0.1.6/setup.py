# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sciebo_rds_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.4,<9.0.0',
 'kubernetes>=21.7.0,<22.0.0',
 'paramiko>=2.9.2,<3.0.0']

entry_points = \
{'console_scripts': ['sciebords = sciebo_rds_cli.main:cli']}

setup_kwargs = {
    'name': 'sciebo-rds-cli',
    'version': '0.1.6',
    'description': 'Script for install sciebo RDS in sciebo',
    'long_description': '[![PyPI version](https://badge.fury.io/py/sciebo-rds-cli.svg)](https://badge.fury.io/py/sciebo-rds-cli)\n\nStatus: not for production, yet\n\n# Sciebo RDS CLI\n\nThis is a helper tool to install sciebo RDS to your owncloud instances. It supports ssh and kubectl.\n\n## Usage\n\nYou need python3 (>= 3.10) and pip to use this tool.\n\n```bash\npip install sciebo-rds-cli\nsciebords --help\n```\n\nIf you prefer the sourcecode way:\n\n```bash\ngit clone https://github.com/Heiss/Sciebo-RDS-Install.git && cd Sciebo-RDS-Install\npip install -r requirements.txt\nchmod +x sciebo_rds_install/main.py\nsciebo_rds_install/main.py --help\n```\n\nIf you have poetry installed, you can use it, too. So the installation will not rubbish your local python environment, because it uses virtualenv on its own.\n\n```bash\ngit clone https://github.com/Heiss/Sciebo-RDS-Install.git && cd Sciebo-RDS-Install\npoetry install\npoetry shell\nsciebords --help\n```\n\nThe application will look for a `values.yaml`, which is needed for the sciebo RDS helm supported installation process. So you only have to maintain a single yaml file. Just append the content of `config.yaml.example` to your `values.yaml`. But you can also set your config stuff for this tool in a separated `config.yaml` with `--config` flag. For options for the configuration, please take a look into the `config.yaml.example`, because it holds everything with documentation you can configure for this app. Also you should take a look into the help parameter, because it shows, what the tool can do for you.\n\n## Developer installation\n\nThis project uses [poetry](https://python-poetry.org/docs/#installation) for dependencies. Install it with the described methods over there in the official poetry documentation.\n\nThen you need to install the developer environment.\n\n```bash\npoetry install --with dev\npoetry shell\n```\n\nAfter this you can run the application in this environment.\n\n```bash\nsciebords --help\n```\n\nIf you add or update the dependencies, you have to generate a new requirementst.txt for easier user installations.\n\n```bash\npoetry export -f requirements.txt --output requirements.txt\n```\n',
    'author': 'Peter Heiss',
    'author_email': 'peter.heiss@uni-muenster.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Sciebo-RDS/Sciebo-RDS-CLI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
