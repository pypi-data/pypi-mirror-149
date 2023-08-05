# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotbee']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'spotipy>=2.19.0,<3.0.0']

setup_kwargs = {
    'name': 'spotbee',
    'version': '1.1.0',
    'description': 'A simple module that converts Spotify Playlists into a list of Youtube URLs',
    'long_description': '# spotbee\n\nThis is a module that spits out YouTube URLs from Spotify Playlist URLs\n\n**Why use this?**\n\nIt is asynchronous which makes it compatible to use with Discord Bots.\n\n**Installation**\n\n```bash\npip install spotbee\n```\n\n**Examples*\n\nCheck the `examples` folder.\n\nCredit to [Samrid Pandit](https://github.com/CaffeineDuck) for the name.\n',
    'author': 'Nishant Sapkota',
    'author_email': 'snishant306@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thenishantsapkota/spotbee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
