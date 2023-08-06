# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napm']

package_data = \
{'': ['*']}

install_requires = \
['gdown>=4.4.0,<5.0.0',
 'loguru>=0.6.0,<0.7.0',
 'omegaconf>=2.1.1,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'napm',
    'version': '0.2.1',
    'description': 'Not A Package Manager.',
    'long_description': None,
    'author': 'David Marx',
    'author_email': 'david.marx84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
