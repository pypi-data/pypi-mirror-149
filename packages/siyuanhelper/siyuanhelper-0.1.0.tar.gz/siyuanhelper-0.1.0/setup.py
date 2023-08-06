# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['siyuanhelper']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'cchardet>=2.1.7,<3.0.0']

setup_kwargs = {
    'name': 'siyuanhelper',
    'version': '0.1.0',
    'description': 'Helper lib for Siyuan Note',
    'long_description': None,
    'author': 'clouder',
    'author_email': 'clouder0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/Clouder0/siyuanhelper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
