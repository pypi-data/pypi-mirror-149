# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_xtdb']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.11.2,<0.12.0',
 'edn-format>=0.7.5,<0.8.0',
 'pampy>=0.3.0,<0.4.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'py-xtdb',
    'version': '0.3.1',
    'description': 'Small functions for interacting with XTDB via http.',
    'long_description': None,
    'author': 'joefromct',
    'author_email': 'joefromct@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
