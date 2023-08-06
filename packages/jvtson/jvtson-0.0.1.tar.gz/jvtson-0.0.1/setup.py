# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jvtson']
setup_kwargs = {
    'name': 'jvtson',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Lawry Lawry',
    'author_email': 'lawrydeeb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
