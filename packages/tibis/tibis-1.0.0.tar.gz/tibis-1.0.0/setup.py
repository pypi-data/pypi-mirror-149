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
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'shoxxdj',
    'author_email': 'shoxx@shoxxdj.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
