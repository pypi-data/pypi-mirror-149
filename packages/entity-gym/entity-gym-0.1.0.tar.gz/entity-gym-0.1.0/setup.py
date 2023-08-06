# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entity_gym',
 'entity_gym.env',
 'entity_gym.examples',
 'entity_gym.serialization',
 'entity_gym.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cloudpickle>=2.0.0,<3.0.0',
 'msgpack-numpy>=0.4.7,<0.5.0',
 'msgpack>=1.0.3,<2.0.0',
 'ragged-buffer>=0.3.9,<0.4.0',
 'tqdm>=4.63.1,<5.0.0']

setup_kwargs = {
    'name': 'entity-gym',
    'version': '0.1.0',
    'description': 'Entity Gym',
    'long_description': None,
    'author': 'Clemens Winter',
    'author_email': 'clemenswinter1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
