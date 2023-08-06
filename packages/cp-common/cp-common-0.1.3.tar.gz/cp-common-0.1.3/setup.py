# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cp_common']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'cp-common',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'zmf963',
    'author_email': 'zmf96@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
