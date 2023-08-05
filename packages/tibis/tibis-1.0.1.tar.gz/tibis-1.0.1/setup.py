# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tibis', 'tibis.lib']

package_data = \
{'': ['*']}

install_requires = \
['PGPy>=0.5.4,<0.6.0',
 'PyYAML>=6.0,<7.0',
 'py-pgp>=0.0.1,<0.0.2',
 'simple-chalk>=0.1.0,<0.2.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['tibis = tibis.tibis:main']}

setup_kwargs = {
    'name': 'tibis',
    'version': '1.0.1',
    'description': '',
    'long_description': "# Tibis\n\n![image](https://user-images.githubusercontent.com/5250807/166554591-47e85ac2-2f59-4e33-ba95-a76f2ea41818.png)\n\n\nTibis (Thot the IBIS) is a tool to help manage encrypted directories (named data container here) \n\nName is inspired by the Egyptian god of writers and protector of knowledge \n\n## TLDR; Setup \n\n```\ngit clone https://github.com/shoxxdj/tibis.git\ncd tibis\npoetry install \n```\n\n## TLDR; Usage \n\n### Create a new data container\n```\ntibis create <name>\n```\nThot will ask you a passphrase, choose a good one !\n\n### List data containers\n```\ntibis list \n```\n\n### Mount a data container \n```\ntibis unlock <name> <destination path>\n```\nThot will ask your passphrase.\n\n### Lock a data container\n```\ntibis lock <name>\n```\nThot will not ask your passphrase.. because it's PGP Public key.\n\n### Remove an entry \n```\ntibis delete <name>\n```\nThot will ask you a confirmation, take care !\n## Why ? \nBecause we have to handle with sensitive files, and store them securly can be boring\n\n## How ? \nTibis is a kind of python wrapper on pgp keys and gzip files. \n\nYes, nothing more. \n\n## Why do we have to set passphrase ? \nSecurity is a matter of trust, if you don't trust your laptop enough to store sensitive data, why leave the keys in it ?\n\nBy using a passphrase, access to the data needs : something you have ( data / key ) and something you know ( passphrase ) \n",
    'author': 'shoxxdj',
    'author_email': 'shoxx@shoxxdj.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shoxxdj/tibis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
