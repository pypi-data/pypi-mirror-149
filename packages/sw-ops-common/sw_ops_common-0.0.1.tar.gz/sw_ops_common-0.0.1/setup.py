# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sw_ops_common', 'sw_ops_common.asyncio', 'sw_ops_common.config']

package_data = \
{'': ['*']}

install_requires = \
['DBUtils==3.0.2',
 'PyMySQL>=1.0.2,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'aiomysql',
 'redis>=4.2.2,<5.0.0']

setup_kwargs = {
    'name': 'sw-ops-common',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'xuxygo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
