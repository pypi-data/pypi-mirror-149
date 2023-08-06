# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['publish_npm']
entry_points = \
{'console_scripts': ['publish-npm = publish_npm:main']}

setup_kwargs = {
    'name': 'publish-npm',
    'version': '1.0.36',
    'description': 'a script to update an NPM package',
    'long_description': None,
    'author': 'Zamiell',
    'author_email': '5511220+Zamiell@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
