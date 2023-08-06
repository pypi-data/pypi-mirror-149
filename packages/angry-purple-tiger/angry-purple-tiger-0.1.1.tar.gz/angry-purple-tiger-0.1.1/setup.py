# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['angry_purple_tiger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'angry-purple-tiger',
    'version': '0.1.1',
    'description': 'Animal-based hash digests for humans',
    'long_description': "# angry-purple-tiger\n\nAnimal-based digests for humans... in Python.\n\n## Overview\n\nAngry Purple Tiger generates animal-based hash digests meant to be memorable and human-readable. Angry Purple Tiger is apt for anthropomorphizing project names, crypto addresses, UUIDs, or any complex string of characters that need to be displayed in a user interface.\n\nThis is a Python port of Helium's original [JavaScript implementation](https://github.com/helium/angry-purple-tiger).\n\n## Installation\n\n`pip install angry-purple-tiger`\n\n## Usage\n\n```python\nfrom angry_purple_tiger.angry_purple_tiger import animal_hash\n\n# input strings (like wallet addresses) must be encoded\nname = animal_hash('112CuoXo7WCcp6GGwDNBo6H5nKXGH45UNJ39iEefdv2mwmnwdFt8'.encode())\n\nprint(name)\n# feisty-glass-dalmation\n```",
    'author': 'Evan Diewald',
    'author_email': 'evandiewald@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evandiewald/angry-purple-tiger-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
