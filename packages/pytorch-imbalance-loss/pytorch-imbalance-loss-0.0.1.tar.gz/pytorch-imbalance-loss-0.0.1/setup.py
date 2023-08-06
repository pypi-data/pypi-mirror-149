# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_imbalance_loss']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.3.2,<0.4.0',
 'numpy>=1.22.3,<2.0.0',
 'torch<=1.9.0',
 'torchtyping>=0.1.4,<0.2.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'pytorch-imbalance-loss',
    'version': '0.0.1',
    'description': 'Imbalance Losses in PyTorch for NLP',
    'long_description': None,
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
