# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworldtidesinfo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'pyworldtidesinfo',
    'version': '3.0.0',
    'description': 'A simple API for world tides info server',
    'long_description': '# pyworldtidesinfo\n## General\n![GitHub release](https://img.shields.io/github/release/jugla/pyWorldtidesinfo)\n\nGet tide info from World Tides Info server :\n- Location Parameter : latitude/longitude of monitored point\n- Tide prediction parameter : reference (LAT,...), tide station distance, tide prediction duration\n- Tide picture : unit (meter/feet), plot/background color\n\n## Installing\n```\npip install pyworldtidesinfo\n```\n\n## Use\n**Prerequisite** : a valid key from https://www.worldtides.info/\n\nThe `__main__.py` is provided to show an example of use.\n\n- 2 main functions to connect to server :\n\n  - retrieve tide station info\n\n  - retrieve tide info (height, ...)\n\n- several functions to decode the receive message from server\n\n\n',
    'author': 'jugla',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jugla/pyWorldtidesinfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.11',
}


setup(**setup_kwargs)
