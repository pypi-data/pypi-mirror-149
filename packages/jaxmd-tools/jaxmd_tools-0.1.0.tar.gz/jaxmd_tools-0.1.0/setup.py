# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaxmd_tools', 'jaxmd_tools._src']

package_data = \
{'': ['*']}

install_requires = \
['ase>=3.22.1,<4.0.0', 'jax-md>=0.1.28,<0.2.0', 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'jaxmd-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Minjoon Hong',
    'author_email': 'mjhong0708@yonsei.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
