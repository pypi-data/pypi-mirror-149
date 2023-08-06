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
    'version': '1.1.0',
    'description': 'Advanced SFTP functions based on Paramiko',
    'long_description': '# sftputil\n\nPython High-level SFTP client library\n\n## Description\n\n`sftputil` is Python library to transfer files using SFTP. At this point only\nthe API is available, but a command line will probably be added in the future.\n\nWhy this package?\n\n- Paramiko provides a\n  [SFTP](https://docs.paramiko.org/en/latest/api/sftp.html#paramiko.sftp_client.SFTPClient)\n  client but it does not contain many methods. It is alright if one only needs\n  simple get/put/list commands. But it is not enough for more complex operations.\n- [pySFTP](https://pypi.org/project/pysftp/) would have been the solution, but\n  it has not been updated since 2016 (at the time of this writing). It is a dead\n  project and cannot be improved. It does not manage the last SSH key\n  algorithms.\n\nThus this new project. The initial reason was also that I needed a `rsync`-like\ncommand through SFTP in Python scripts.\n\n## Installation\n\nAvailable on [pypi](https://pypi.org/project/sftputil/).\n\n```\npip install sftputil\n```\n\n## Usage\n\nTODO\n\n## Support\n\nIf you have any question or suggestion, you can open a new\n[issue](https://framagit.org/RomainTT/sftputil/-/issues).\n\n## Roadmap\n\nTODO for future releases:\n\n- Add synchronisation on the other direction (push)\n- Add a command line\n- Add some unit tests\n\n## Contributing\n\nYou are free to fork this repository and to do Merge Requests that I will\nreview.\n\n## Authors and acknowledgment\n\nMain author: Romain TAPREST <romain@taprest.fr>\n\n## License\n\nLicensed under [Mozilla Public License v2](./LICENSE).\n\n## Project status\n\nAlive! 💓\n',
    'author': 'Romain TAPREST',
    'author_email': 'romain@taprest.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/RomainTT/sftputil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
