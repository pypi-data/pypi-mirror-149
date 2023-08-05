# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockeree']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0',
 'docker>=4.4.0',
 'loguru>=0.6.0',
 'networkx>=2.5',
 'pandas>=1.2.0',
 'pygit2>=1.9.1',
 'pytest>=3.0',
 'requests>=2.20.0']

setup_kwargs = {
    'name': 'dockeree',
    'version': '0.1.0',
    'description': 'Make it easy to build and manager Docker images.',
    'long_description': None,
    'author': 'Benjamin Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
