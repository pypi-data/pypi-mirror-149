# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['explicit_nlu',
 'explicit_nlu.__test__',
 'explicit_nlu.api',
 'explicit_nlu.evaluator',
 'explicit_nlu.extractor',
 'explicit_nlu.extractor.binding',
 'explicit_nlu.listener',
 'explicit_nlu.parser',
 'explicit_nlu.parser.xml',
 'explicit_nlu.parser.xml.__test__',
 'explicit_nlu.token',
 'explicit_nlu.token.tokenizer',
 'explicit_nlu.token.tokenizer.__test__']

package_data = \
{'': ['*'],
 'explicit_nlu': ['antlr/*', 'visitor/*'],
 'explicit_nlu.api': ['support/*']}

install_requires = \
['antlr4-python3-runtime>=4.8,<5.0']

entry_points = \
{'console_scripts': ['build = poetry_scripts:build',
                     'clean = poetry_scripts:clean',
                     'install = poetry_scripts:install',
                     'publish = poetry_scripts:publish',
                     'test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'explicit-nlu',
    'version': '0.10.6',
    'description': 'Explicit is a cross platform library for rule based named entity recognition.',
    'long_description': None,
    'author': 'Leftshift One',
    'author_email': 'contact@leftshift.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
