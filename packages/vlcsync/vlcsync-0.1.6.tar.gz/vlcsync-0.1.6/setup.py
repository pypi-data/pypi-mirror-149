# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlcsync']

package_data = \
{'': ['*']}

install_requires = \
['cached-property', 'loguru', 'psutil']

entry_points = \
{'console_scripts': ['vlcsync = vlcsync.main:main']}

setup_kwargs = {
    'name': 'vlcsync',
    'version': '0.1.6',
    'description': 'Utility for synchronize multiple instances of VLC. Supports seek, play and pause. ',
    'long_description': 'VLC Sync\n========\n\nUtility for synchronize multiple instances of VLC. Supports seek, play and pause. \nInspired by F1 streams with extra driver tracking data.  \n\nMotivation:\n\nDid [not find](#alternatives) reasonable alternative for Linux. \nSo decided to write my own solution.\n\nCurrently, tested on Linux, Windows 7/10 (macOS should also work).\n\n## Install\n\n```shell\npip3 install -U vlcsync\n```\n\nor \n\nDownload [binary release](https://github.com/mrkeuz/vlcsync/releases) (Windows)\n\n## Run\n\n`Vlc` players should open with `--rc-host 127.0.0.42` option OR configured properly from gui (see [how configure vlc](./docs/vlc_setup.md)) \n\n```shell\n\n# Run vlc players \n$ vlc --rc-host 127.0.0.42 SomeMedia1.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia2.mkv &\n$ vlc --rc-host 127.0.0.42 SomeMedia3.mkv &\n\n# Vlcsync will monitor all vlc players and do syncing \n$ vlcsync\n```\n\n## Demo\n\n![vlcsync](./docs/vlcsync.gif)\n\n## Alternatives\n\n- [vlc](https://www.videolan.org/vlc/index.ru.html) \n    - Open additional media. Seems feature broken in vlc 3 (also afaik limited only 2 instances)  \n    - There is a [netsync](https://wiki.videolan.org/Documentation:Modules/netsync/) but seem only master-slave (not tried)\n- [Syncplay](https://github.com/Syncplay/syncplay) - very promised, but little [complicated](https://github.com/Syncplay/syncplay/discussions/463) for my case\n- [bino](https://bino3d.org/) - working, buy very strange controls, file dialog not working and only fullscreen\n- [gridplayer](https://github.com/vzhd1701/gridplayer) - low fps by some reason\n\n## Contributing\n\nAny thoughts, ideas and contributions welcome!  \n\nEnjoy! 🚀\n',
    'author': 'mrkeuz',
    'author_email': 'mrkeuz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrkeuz/vlcsync/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
