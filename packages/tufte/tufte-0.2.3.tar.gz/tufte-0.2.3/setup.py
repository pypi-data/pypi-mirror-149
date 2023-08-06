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
    'version': '0.2.3',
    'description': 'A Tufte-inspired style for plotting data',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/tufte/badge/?version=latest)](https://tufte.readthedocs.io/en/latest/?badge=latest)\n[![CI](https://github.com/hsteinshiromoto/tufte/actions/workflows/ci.yml/badge.svg)](https://github.com/hsteinshiromoto/tufte/actions/workflows/ci.yml)\n[![Github tag](https://badgen.net/github/tag/hsteinshiromoto/tufte)](https://github.com/hsteinshiromoto/tufte/tags/)\n[![PyPI version](https://badge.fury.io/py/tufte.svg)](https://badge.fury.io/py/tufte)\n[![DOI](https://zenodo.org/badge/130211437.svg)](https://zenodo.org/badge/latestdoi/130211437)\n\n# 1. Tufte\n\nA Tufte-inspired style for plotting data.\n\n# 2. Table of Contents\n\n- [1. Tufte](#1-tufte)\n- [2. Table of Contents](#2-table-of-contents)\n- [3. Installation](#3-installation)\n\n# 3. Installation\n\n`$ pip install tufte`',
    'author': 'Humberto STEIN SHIROMOTO',
    'author_email': 'h.stein.shiromoto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hsteinshiromoto/tufte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
