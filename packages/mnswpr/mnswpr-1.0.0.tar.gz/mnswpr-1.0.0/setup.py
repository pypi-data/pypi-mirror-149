# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mnswpr']
install_requires = \
['numpy>=1.18.5,<2.0.0']

entry_points = \
{'console_scripts': ['mnswpr = mnswpr:main']}

setup_kwargs = {
    'name': 'mnswpr',
    'version': '1.0.0',
    'description': 'minesweeper',
    'long_description': None,
    'author': 'worldmaker',
    'author_email': 'worldmaker18349276@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
