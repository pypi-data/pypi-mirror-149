# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wanda']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['wanda = wanda.wanda:run']}

setup_kwargs = {
    'name': 'wanda',
    'version': '0.56',
    'description': 'Set wallpapers with keywords or randomly',
    'long_description': None,
    'author': 'kshib',
    'author_email': 'ksyko@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
