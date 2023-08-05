# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookmark']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bm = bookmark.cli:main']}

setup_kwargs = {
    'name': 'bookmark-cli',
    'version': '0.0.4',
    'description': 'command line for bookmark',
    'long_description': None,
    'author': 'wxnacy',
    'author_email': 'wxnacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
