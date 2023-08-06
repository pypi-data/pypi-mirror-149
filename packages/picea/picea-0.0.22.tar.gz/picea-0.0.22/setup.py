# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picea']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.2,<2.0.0']

setup_kwargs = {
    'name': 'picea',
    'version': '0.0.22',
    'description': 'A lightweight python library for working with trees and biological sequence collections',
    'long_description': "# _picea_\n\nLightweight python library for working with trees and sequence collections\n\n[![CI](https://github.com/holmrenser/picea/actions/workflows/ci.yml/badge.svg)](https://github.com/holmrenser/picea/actions/workflows/ci.yml)\n![docs](https://github.com/holmrenser/picea/workflows/docs/badge.svg?branch=master)\n[![Coverage Status](https://coveralls.io/repos/github/holmrenser/picea/badge.svg?branch=master)](https://coveralls.io/github/holmrenser/picea?branch=master)\n[![PyPI version](https://badge.fury.io/py/picea.svg)](https://badge.fury.io/py/picea)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/picea.svg)](https://pypi.python.org/pypi/ansicolortags/)\n[![PyPI status](https://img.shields.io/pypi/status/picea.svg)](https://pypi.python.org/pypi/ansicolortags/)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n```\npip install picea\n```\n\n![example figure](https://github.com/holmrenser/picea/raw/master/docs/example1.png)\n\nThe above figure can be generated with the following code\n\n```python\nfrom picea import Tree, treeplot\nimport matplotlib.pyplot as plt\n\nnewick = '(((a,b),(c,d)),e)'\ntree = Tree.from_newick(newick)\n\nfig, (ax1, ax2) = plt.subplots(ncols = 2, figsize = (10, 4))\n\n#left-to-right layout with direct links\ntreeplot(tree, style='rectangular', ltr=True, ax=ax1)\n\n#right-to-left layout with square links\ntreeplot(tree, style='square', ltr=False, ax=ax2)\n```\n",
    'author': 'Rens Holmer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/holmrenser/picea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
