# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spdstrlib']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'spdstrlib',
    'version': '0.1.34',
    'description': 'Speedster application project library manager.',
    'long_description': None,
    'author': 'Diogo André',
    'author_email': 'das.dias6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
