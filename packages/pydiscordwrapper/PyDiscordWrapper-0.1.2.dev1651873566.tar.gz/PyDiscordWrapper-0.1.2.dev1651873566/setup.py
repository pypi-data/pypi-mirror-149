# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydiscordwrapper', 'pydiscordwrapper.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0']}

setup_kwargs = {
    'name': 'pydiscordwrapper',
    'version': '0.1.2.dev1651873566',
    'description': 'A simple wrapper for the Discord API for Python using async/non async methods with httpx and pydantic.',
    'long_description': '# PyDiscordWrapper [![Tests](https://github.com/MarcoMuellner/PyDiscordWrapper/workflows/Tests/badge.svg)](https://github.com/<your-username>/hypermodern-python/actions?workflow=Tests)\n\nA simple http async/non async wrapper around the discord API using httpx and pydantic\n',
    'author': 'Marco Müllner',
    'author_email': 'muellnermarco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarcoMuellner/PyDiscordWrapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
