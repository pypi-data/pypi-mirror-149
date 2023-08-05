# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tufte']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'tufte',
    'version': '0.2.2',
    'description': 'A Tufte-inspired style for plotting data',
    'long_description': None,
    'author': 'Humberto STEIN SHIROMOTO',
    'author_email': 'h.stein.shiromoto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
