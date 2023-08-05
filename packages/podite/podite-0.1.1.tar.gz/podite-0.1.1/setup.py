# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['podite', 'podite.types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'podite',
    'version': '0.1.1',
    'description': 'What you see is what you get serialization for Plain Old Data',
    'long_description': None,
    'author': 'Nima Hamidi',
    'author_email': 'hamidi@alumni.stanford.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JumpCrypto/podite',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
