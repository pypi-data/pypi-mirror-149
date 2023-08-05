# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'mcfa>=0.1,<0.2',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'rich>=12.2.0,<13.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4', 'sphinx-redactor-theme>=0.0.1,<0.0.2']}

setup_kwargs = {
    'name': 'space-classy',
    'version': '0.2',
    'description': 'classification tool for minor bodies using reflectance spectra and visual albedos',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/space-classy) [![arXiv](https://img.shields.io/badge/arXiv-2203.11229-f9f107.svg)](https://arxiv.org/abs/2203.11229) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n<p align="center">\n  <img width="260" src="https://raw.githubusercontent.com/maxmahlke/classy/main/docs/gfx/logo_classy.png">\n</p>\n\n[Features](#features) - [Install](#install) - [Documentation](#documentation)\n\nClassify asteroids in the taxonomic scheme by [Mahlke, Carry, Mattei 2020](https://arxiv.org/abs/2203.11229).\nbased on reflectance spectra and visual albedos using the command line.\n\n``` sh\n\n$ classy classify path/to/observations.csv\n\n```\n\nor do it step-by-step\n\n``` sh\n\n$ classy preprocess path/to/observations.csv\n\n```\n\nTip: Check out [rocks](https://github.com/maxmahlke/rocks) to easily add IAU\nnames, numbers, designations, and literature parameters to the observations.\n\n<!-- # Install -->\n\n<!-- `classy` is available on the [python package index](https://pypi.org) as *space-classy*: -->\n\n<!-- ``` sh -->\n<!-- $ pip install space-classy -->\n<!-- ``` -->\n\n<!-- # Documentation -->\n\n<!-- Check out the documentation at [classy.readthedocs.io](https://classy.readthedocs.io/en/latest/). -->\nor run\n\n     $ classy docs\n\n<!-- # Contribute -->\n\n<!-- Automatic determination of best smoothing parameters -->\n<!-- Computation of asteroid class by weighted average -->\n',
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmahlke/classy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
