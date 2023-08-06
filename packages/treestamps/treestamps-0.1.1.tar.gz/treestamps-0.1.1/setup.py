# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'tests.unit']

package_data = \
{'': ['*']}

modules = \
['treestamps']
install_requires = \
['ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'treestamps',
    'version': '0.1.1',
    'description': 'Create timestamp records for recursive operations on directory trees.',
    'long_description': '# Treestamps\n\nA library to set and retrieve timestamps to speed up operations\nrun recursively on directory trees.\n\nPrincipal methodds on the Treestamps class are: init(), get(), set(), dump().\nA factory method is also provided for creating top path to Treestamp maps.\n\nDocumentation is to read the code for now.\n',
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/treestamps',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
