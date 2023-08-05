# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deluge_cmd', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'deluge-card==0.3.0']

entry_points = \
{'console_scripts': ['dsd = deluge_cmd.deluge_dsd:main']}

setup_kwargs = {
    'name': 'deluge-cmd',
    'version': '0.2.0',
    'description': 'Command line tools to manage Synthstrom deluge SD card contents.',
    'long_description': '# deluge-cmd\n\n[![pypi](https://img.shields.io/pypi/v/deluge-cmd.svg)](https://pypi.org/project/deluge-cmd/)\n[![python](https://img.shields.io/pypi/pyversions/deluge-cmd.svg)](https://pypi.org/project/deluge-cmd/)\n[![Build Status](https://github.com/mupaduw/deluge-cmd/actions/workflows/dev.yml/badge.svg)](https://github.com/mupaduw/deluge-cmd/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/mupaduw/deluge-cmd/branch/main/graphs/badge.svg)](https://codecov.io/github/mupaduw/deluge-cmd)\n\n\nSome cli tools to manage Synthstrom Deluge SD card contents.\n\n* Documentation: <https://mupaduw.github.io/deluge-cmd>\n* GitHub: <https://github.com/mupaduw/deluge-cmd>\n* PyPI: <https://pypi.org/project/deluge-cmd/>\n* Free software: MIT\n\nThis project uses [deluge-card](https://github.com/mupaduw/deluge-card) which provides a python API for the Deluge Folder System.\n\n## Features\n\n- list Songs Samples, and Song Samples on a Deluge Folder System (DFS).\n- check Deluge Folder Systems.\n- list useful attributes tempo, key, scale.\n- filter on path patterns: e.g. list all "Kick" samples).\n\ne.g.\n\n```\n>$ dls ~/Music/DELUGE/01 songs -p *001*\nDeluge filesystem at /homie/Music/DELUGE/01 mounted: False\n  DelugeSong(/homie/Music/DELUGE/01/SONGS/SONG001.XML) key C major tempo 96.0\n  DelugeSong(/homie/Music/DELUGE/01/SONGS/SONG001A.XML) key C major tempo 96.0\n  DelugeSong(/homie/Music/DELUGE/01/SONGS/SONG001B.XML) key C major tempo 108.0\n  DelugeSong(/homie/Music/DELUGE/01/SONGS/SONG001C.XML) key C major tempo 108.0\n  DelugeSong(/homie/Music/DELUGE/01/SONGS/SONG001D.XML) key C major tempo 96.0\n```\n\n### Planned features\n- (d)cp, (d)mv and (d)rm commands.\n- song groups (1, 1A, 1B, 1C).\n- instruments, kits & synths.\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
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
