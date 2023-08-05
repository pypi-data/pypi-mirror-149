# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monkeytale']

package_data = \
{'': ['*']}

install_requires = \
['NRCLex>=3.0.0,<4.0.0',
 'click>=8.0.0,<9.0.0',
 'identify>=2.5.0,<3.0.0',
 'keyring>=23.5.0,<24.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'sh>=1.14.2,<2.0.0',
 'spacy>=3.3.0,<4.0.0',
 'textX>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['@ = src.__ini__:cli', 'monkeytale = src.__init__:cli']}

setup_kwargs = {
    'name': 'monkeytale',
    'version': '0.2.0',
    'description': 'An opinionated markup language for composing, documenting, and visualizing a novel.',
    'long_description': '# Monkeytale v0.2.0\n\nMonkeytale is a markup language for composing, documenting, and visualizing a novel from flat files. It is built to meet my needs and, thus, opinionated to a fault.\n\n[Semantic Versioning](https://semver.org/) and [Semantic Release](https://pypi.org/project/python-semantic-release/) help track progress with Monkeytale.\n\nAs per Semantic Versioning: "Major version zero (0.y.z) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable."\n\nSome documentation may be written when Monkeytale is mature and stable.\n',
    'author': 'Monkeytail',
    'author_email': 'monkeytail@dwlib.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
