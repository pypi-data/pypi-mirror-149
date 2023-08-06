# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msg2po']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.2.0',
 'natsort>=6.2.1,<7',
 'polib>=1.1.1',
 'python-dateutil>=2.8.2',
 'ruamel.yaml>=0.17.21']

entry_points = \
{'console_scripts': ['bgforge-config = msg2po.bgforge-config:main',
                     'dir2msgstr = msg2po.dir2msgstr:main',
                     'file2msgstr = msg2po.file2msgstr:main',
                     'file2po = msg2po.file2po:main',
                     'msgmerge-female = msg2po.msgmerge:main',
                     'po2file = msg2po.po2file:main',
                     'resave-po = msg2po.resave-po:main',
                     'unpoify = msg2po.unpoify:main']}

setup_kwargs = {
    'name': 'msg2po',
    'version': '1.1.1',
    'description': 'A set of helper tools to convert Fallout 1/2 MSG and WeiDU TRA into GNU gettext PO and back',
    'long_description': '# MSG2PO\n\n[![Build status](https://github.com/BGforgeNet/msg2po/workflows/release/badge.svg)](https://github.com/BGforgeNet/msg2po/actions?query=workflow%3Arelease)\n[![Patreon](https://img.shields.io/badge/Patreon-donate-FF424D?logo=Patreon&labelColor=141518)](https://www.patreon.com/BGforge)\n[![Telegram](https://img.shields.io/badge/telegram-join%20%20%20%20%E2%9D%B1%E2%9D%B1%E2%9D%B1-darkorange?logo=telegram)](https://t.me/bgforge)\n[![Discord](https://img.shields.io/discord/420268540700917760?logo=discord&label=discord&color=blue&logoColor=FEE75C)](https://discord.gg/4Yqfggm)\n[![IRC](https://img.shields.io/badge/%23IRC-join%20%20%20%20%E2%9D%B1%E2%9D%B1%E2%9D%B1-darkorange)](https://bgforge.net/irc)\n\nThis is a set of tools to convert Fallout 1/2 MSG and WeiDU TRA into GNU gettext PO and back, used in [BGforge Hive](https://hive.bgforge.net/). Ask questions [here](https://forums.bgforge.net/viewforum.php?f=9).\n\n## Installation\n```bash\npip install msg2po\n```\n\n## Usage\n```\npoify -h\nunpoify -h\nmsgmerge-female -h\nfile2po -h\npo2file -h\nfile2msgstr -h\ndir2msgstr -h\n```\n\n## Action\nGithub [action](docs/action.md) is available for automatic processing.\n\n---\n[Changelog](docs/changelog.md)\n',
    'author': 'BGforge',
    'author_email': 'dev@bgforge.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BGforgeNet/msg2po',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
