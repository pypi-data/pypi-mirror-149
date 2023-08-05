# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sftputil']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'sftputil',
    'version': '1.0.0',
    'description': 'Advanced SFTP functions based on Paramiko',
    'long_description': None,
    'author': 'Romain TAPREST',
    'author_email': 'romain@taprest.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
