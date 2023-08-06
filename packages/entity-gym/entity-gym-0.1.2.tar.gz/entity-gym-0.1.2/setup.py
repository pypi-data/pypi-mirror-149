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
    'version': '0.1.2',
    'description': 'Entity Gym',
    'long_description': '# Entity Gym\n\n[![Actions Status](https://github.com/entity-neural-network/incubator/workflows/Test/badge.svg)](https://github.com/entity-neural-network/incubator/actions)\n[![PyPI](https://img.shields.io/pypi/v/entity-gym.svg?style=flat-square)](https://pypi.org/project/entity-gym/)\n[![Documentation Status](https://readthedocs.org/projects/entity-gym/badge/?version=latest&style=flat-square)](https://entity-gym.readthedocs.io/en/latest/?badge=latest)\n[![Discord](https://img.shields.io/discord/913497968701747270?style=flat-square)](https://discord.gg/SjVqhSW4Qf)\n\n\nEntity Gym is an open source Python library that defines an _entity based_ API for reinforcement learning environments.\nEntity Gym extends the standard paradigm of fixed-size observation spaces by allowing observations to contain dynamically-sized lists of entities.\nThis enables a seamless and highly efficient interface with simulators, games, and other complex environments whose state can be naturally expressed as a collection of entities.\n\nThe [ENN-PPO library](https://github.com/entity-neural-network/incubator/tree/main/enn_ppo) can be used to train agents for Entity Gym environments.\n\n## Installation\n\n```\npip install entity-gym\n```\n\n## Usage\n\nYou can find tutorials, guides, and an API reference on the [Entity Gym documentation website](https://entity-gym.readthedocs.io/en/latest/index.html).\n\n## Examples\n\nA number of simple example environments can be found in [entity_gym/examples](https://github.com/entity-neural-network/incubator/tree/main/entity_gym/entity_gym/examples). The [ENN-Zoo](https://github.com/entity-neural-network/incubator/tree/main/enn_zoo/enn_zoo) project implements Entity Gym bindings for [Procgen](https://github.com/openai/procgen), [Griddly](https://github.com/Bam4d/Griddly), [MicroRTS](https://github.com/santiontanon/microrts), [VizDoom](https://github.com/mwydmuch/ViZDoom), and [CodeCraft](https://github.com/cswinter/DeepCodeCraft).\n',
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
