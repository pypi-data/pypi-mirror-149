# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_cli_recorder', 'sphinx_cli_recorder.testing']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Sphinx>=4.4.0,<5.0.0',
 'asciinema>=2.2.0,<3.0.0',
 'asyncer>=0.0.1,<0.0.2',
 'pexpect>=4.8.0,<5.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'unsync>=1.4.0,<2.0.0',
 'yamale>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'sphinx-cli-recorder',
    'version': '0.1.3',
    'description': 'A Sphinx extension that runs/automates recordings of CLI applications, without requiring any external services.',
    'long_description': '# Sphinx CLI Recorder\n\n[Please take a look at the official documentation](kai-tub.github.io/sphinx-cli-recorder).\n',
    'author': 'Kai Norman Clasen',
    'author_email': 'k.clasen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai-tub/sphinx_cli_recorder/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
