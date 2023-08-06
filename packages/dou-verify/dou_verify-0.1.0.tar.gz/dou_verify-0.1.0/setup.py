# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dou_verify']

package_data = \
{'': ['*']}

install_requires = \
['pyquery>=1.4.3,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dou-verify',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'satoru',
    'author_email': 'satorulogic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
