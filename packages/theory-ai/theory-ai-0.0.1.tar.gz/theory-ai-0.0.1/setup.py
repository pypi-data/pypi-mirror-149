# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theory_ai']

package_data = \
{'': ['*']}

install_requires = \
['simple-parsing>=0.0.19,<0.0.20']

setup_kwargs = {
    'name': 'theory-ai',
    'version': '0.0.1',
    'description': 'Cloud native machine learning primitives',
    'long_description': None,
    'author': 'Sole Ahab',
    'author_email': 'old.ocean.creature@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
