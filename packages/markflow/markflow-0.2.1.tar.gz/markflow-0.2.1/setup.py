# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markflow', 'markflow._utils', 'markflow.detectors', 'markflow.formatters']

package_data = \
{'': ['*']}

install_requires = \
['pygments', 'rich']

entry_points = \
{'console_scripts': ['markflow = markflow.__main__:__main__']}

setup_kwargs = {
    'name': 'markflow',
    'version': '0.2.1',
    'description': 'Make your Markdown Sparkle!',
    'long_description': None,
    'author': 'Joshua Holland',
    'author_email': 'jholland@duosecurity.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
