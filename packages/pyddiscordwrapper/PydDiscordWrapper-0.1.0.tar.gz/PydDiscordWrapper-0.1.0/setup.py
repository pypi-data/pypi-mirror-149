# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyddiscordwrapper', 'pyddiscordwrapper.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'pyddiscordwrapper',
    'version': '0.1.0',
    'description': 'A simple wrapper for the Discord API for Python using async/non async methods with httpx and pydantic.',
    'long_description': '# PyDiscordWrapper\nA simple http async/non async wrapper around the discord API using httpx and pydantic\n',
    'author': 'Marco Müllner',
    'author_email': 'muellnermarco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarcoMuellner/PyDiscordWrapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
