# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raiden_synapse_modules', 'raiden_synapse_modules.presence_router']

package_data = \
{'': ['*']}

install_requires = \
['coincurve>=15.0.0,<16.0.0', 'raiden-contracts>=0.50.1,<0.51.0']

setup_kwargs = {
    'name': 'raiden-synapse-modules',
    'version': '0.1.4',
    'description': 'synapse modules for the Raiden network',
    'long_description': None,
    'author': 'Brainbot Labs Est.',
    'author_email': 'contact@brainbot.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
