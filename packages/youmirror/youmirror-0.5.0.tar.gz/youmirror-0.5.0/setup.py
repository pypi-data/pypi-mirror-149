# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youmirror']

package_data = \
{'': ['*']}

install_requires = \
['sqlitedict==2.0.0', 'toml>=0.10.2,<0.11.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['youmirror = youmirror.cli:main']}

setup_kwargs = {
    'name': 'youmirror',
    'version': '0.5.0',
    'description': 'Create a mirror filetree of your favorite youtube videos',
    'long_description': None,
    'author': 'wkrettek',
    'author_email': 'warrenkrettek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
