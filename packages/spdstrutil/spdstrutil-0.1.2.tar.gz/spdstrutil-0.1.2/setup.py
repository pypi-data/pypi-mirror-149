# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spdstrutil']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'spdstrutil',
    'version': '0.1.2',
    'description': 'Speedster application utilities package.',
    'long_description': None,
    'author': 'dasdias',
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
