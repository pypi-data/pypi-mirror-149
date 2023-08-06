# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inmanta_module_factory',
 'inmanta_module_factory.helpers',
 'inmanta_module_factory.inmanta',
 'inmanta_module_factory.stats']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'cookiecutter>=1.7.3,<2.0.0', 'inmanta-core>=6.0.1,<7.0.0']

setup_kwargs = {
    'name': 'inmanta-module-factory',
    'version': '2.2.0',
    'description': 'Library for building inmanta modules with python code',
    'long_description': None,
    'author': 'Inmanta',
    'author_email': 'code@inmanta.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
