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
    'version': '0.1.0',
    'description': '1Password CLI helper',
    'long_description': None,
    'author': 'Antoine POPINEAU',
    'author_email': 'antoine@popineau.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
