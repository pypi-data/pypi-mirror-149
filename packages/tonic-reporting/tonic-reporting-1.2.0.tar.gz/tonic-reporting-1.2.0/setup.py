# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tonic_reporting']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0',
 'numpy>=1.0.0,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'scikit-learn>=1.0.0,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'tonic-reporting',
    'version': '1.2.0',
    'description': 'Tools for evaluating fidelity and privacy of synthetic data',
    'long_description': '# Overview\nThis library contains tools for evaluating fidelity and privacy of synthetic data.\n',
    'author': 'Ander Steele',
    'author_email': 'ander@tonic.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.tonic.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
