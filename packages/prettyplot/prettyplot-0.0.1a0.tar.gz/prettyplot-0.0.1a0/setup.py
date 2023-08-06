# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prettyplot']

package_data = \
{'': ['*'], 'prettyplot': ['styles/*']}

install_requires = \
['matplotlib>=3.2,<4.0', 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'prettyplot',
    'version': '0.0.1a0',
    'description': 'Python package for astonishing and bold plots',
    'long_description': None,
    'author': 'Cristiano Moraes Bilacchi',
    'author_email': 'cristiano.bilacchi@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
