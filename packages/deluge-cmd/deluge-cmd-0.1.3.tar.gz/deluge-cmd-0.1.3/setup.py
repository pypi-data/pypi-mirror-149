# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deluge_cmd', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'deluge-card>=0.2.3,<0.3.0']

entry_points = \
{'console_scripts': ['deluge_cmd = deluge_cmd.cli:main',
                     'dsd = deluge_cmd.deluge_cmd.sdu:main']}

setup_kwargs = {
    'name': 'deluge-cmd',
    'version': '0.1.3',
    'description': 'Command line tools to manage Synthstrom deluge SD card contents.',
    'long_description': '# deluge-cmd\n\n\n[![pypi](https://img.shields.io/pypi/v/deluge-cmd.svg)](https://pypi.org/project/deluge-cmd/)\n[![python](https://img.shields.io/pypi/pyversions/deluge-cmd.svg)](https://pypi.org/project/deluge-cmd/)\n[![Build Status](https://github.com/mupaduw/deluge-cmd/actions/workflows/dev.yml/badge.svg)](https://github.com/mupaduw/deluge-cmd/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/mupaduw/deluge-cmd/branch/main/graphs/badge.svg)](https://codecov.io/github/mupaduw/deluge-cmd)\n\n\nSome cli tools to manage Synthstrom Deluge SD card contents.\n\n* Documentation: <https://mupaduw.github.io/deluge-cmd>\n* GitHub: <https://github.com/mupaduw/deluge-cmd>\n* PyPI: <https://pypi.org/project/deluge-cmd/>\n* Free software: MIT\n\n\n## Features\n\n- verify Deluge Filesytem structure\n- list songs \n- list song attributes bpm, key, samples\n- list samples (used/unused)\n\n### Planned features\n- move songs, samples \n- delete songs, samples\n- posix-like glob filtering for list, move & delete\n- list instruments and types\n- anything helpful for backward/forward migration of deluge SD cards having fw3.15 and 4.0 content.\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Chris B Chamberlain',
    'author_email': 'chrisbc@artisan.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mupaduw/deluge-cmd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
