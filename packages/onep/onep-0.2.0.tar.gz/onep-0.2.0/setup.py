# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onep', 'onep.commands']

package_data = \
{'': ['*']}

install_requires = \
['inquirer>=2.9.2,<3.0.0', 'keyring>=23.5.0,<24.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['1p = onep.onep:main']}

setup_kwargs = {
    'name': 'onep',
    'version': '0.2.0',
    'description': '1Password CLI helper',
    'long_description': "# 1p - 1Password CLI helper\n\n`1p` is a wrapper around 1Password's `op` CLI tool to give a more user-friendly interface to secret retrieval.\n\nRequires Python >= 3.7.\n\nIt opens a session with 1Password and stores the session token in the system's keyring, optionally, you can run with `ONEP_SECRET_BACKEND=plain` to store it under `~/.cache/1p`.\n\nIt requires that the configured 1Password account has a shorthand defined (when using `op account add`).\n\n## Installation\n\n```shell\n$ # From PyPI\n$ pip install onep\n\n$ # Development build from GitHub\n$ https://github.com/apognu/1p/releases/download/tip/onep-tip-py3-none-any.whl\n```\n\n## Usage\n\n```shell\n$ 1p --help\nusage: 1p [-h] [-j] ACCOUNT COMMAND ...\n\npositional arguments:\n  ACCOUNT\n  COMMAND\n    signin    Authenticate into a 1Password account\n    vaults    List available vaults\n    vault     Show information about a vault\n    search    Search entries matching provided term\n    show      Display an entry\n    share     Get a shareable link to an item\n\noptions:\n  -h, --help  show this help message and exit\n  -j, --json\n\n$ 1p personal search -t social\nID                            TITLE\n__________________________    GitHub\n__________________________    Twitter\n```\n",
    'author': 'Antoine POPINEAU',
    'author_email': 'antoine@popineau.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/apognu/1p',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
