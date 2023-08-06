# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrpan']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'asyncpraw>=7.5.0,<8.0.0',
 'expiringdict>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'pyrpan',
    'version': '1.0.2a0',
    'description': 'An API wrapper for interacting with the RPAN API.',
    'long_description': '<p>\n<a href="https://pypi.org/project/PyRPAN">\n    <img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/PyRPAN">\n</a>\n\n<a href="https://pypi.org/project/flake8/">\n    <img height="20" alt="Flake badge" src="https://img.shields.io/badge/code%20style-flake8-blue.svg">\n</a>\n</p>\n\n### About\n\nPyRPAN is an async API wrapper made in Python for the Reddit Public Access Network (RPAN), which is Reddit\'s streaming service.\n\n### Example\n\n```Python\nimport asyncio\n\nfrom pyrpan import PyRPAN\n\nrpan = PyRPAN(client_id=\'client id here\', client_secret=\'client secret here\')\n\nasync def main():\n    broadcasts = await rpan.get_broadcast(id=\'stream id here\')  \n    print(broadcast.url)\n\n    await rpan.close()\n\nasyncio.run(main())\n```\n\n### Links\n**Source Code**: [github.com/b1uejay27/PyRPAN](https://github.com/b1uejay27/PyRPAN)<br>\n**PyPi**: [pypi.org/project/PyRPAN](https://pypi.org/project/PyRPAN)<br>\n**Discord Server**: [discord.gg/DfBp4x4](https://discord.gg/DfBp4x4)\n',
    'author': 'b1uejay27',
    'author_email': 'hello@b1uejay27.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b1uejay27/PyRPAN',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
