# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['keton',
 'keton.ai',
 'keton.ai.torch',
 'keton.ai.torch.models',
 'keton.ai.torch.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'keton',
    'version': '0.1.2',
    'description': 'Tools',
    'long_description': None,
    'author': 'Hugh Jiang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
