# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nfem']

package_data = \
{'': ['*'], 'nfem': ['html/*']}

install_requires = \
['plotly>=5.5.0,<6.0.0', 'typing-extensions']

extras_require = \
{':python_version < "3.10"': ['numpy>=1.20,<2.0', 'scipy>=1.4,<2.0'],
 ':python_version < "3.8"': ['notebook>=5.3,<6.0',
                             'importlib-metadata>=4.11,<5.0'],
 ':python_version >= "3.10"': ['numpy>=1.22,<2.0'],
 ':python_version >= "3.10" and python_version < "3.11"': ['scipy>=1.7.2,<2.0.0'],
 ':python_version >= "3.8"': ['notebook>=6.4,<7.0']}

setup_kwargs = {
    'name': 'nfem',
    'version': '4.1.8',
    'description': 'NFEM Teaching Tool',
    'long_description': '# NFEM Teaching Tool\n\n![PyPI](https://img.shields.io/pypi/v/nfem) ![PyPI - Downloads](https://img.shields.io/pypi/dm/nfem) [![Coverage Status](https://coveralls.io/repos/github/StatikTUM/nfem/badge.svg?branch=master&service=github)](https://coveralls.io/github/StatikTUM/nfem?branch=master) ![CI](https://github.com/StatikTUM/nfem/workflows/CI/badge.svg) [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/StatikTUM/nfem/master?filepath=examples) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/StatikTUM/nfem/)\n\nThis is a lightweight python tool build for teaching non linear FEM analysis of 3D truss structures.\n\n## Installation\n\nInstall [Anaconda](https://www.anaconda.com/distribution/), open the Anaconda console and execute the following command:\n\n```shell\npip install nfem\n```\n',
    'author': 'Thomas Oberbichler',
    'author_email': 'thomas.oberbichler@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/StatikTUM/nfem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
