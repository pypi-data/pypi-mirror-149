# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solocast']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['solocast = solocast.solocast:cli']}

setup_kwargs = {
    'name': 'solocast',
    'version': '0.1.5',
    'description': 'Record audio one segment at a time',
    'long_description': None,
    'author': 'Todd Norris',
    'author_email': 'norrist@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/norrist/solocast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
