# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamicrender',
 'dynamicrender.DynamicChecker',
 'dynamicrender.Logger',
 'dynamicrender.Renderer']

package_data = \
{'': ['*'], 'dynamicrender': ['Static/Font/*', 'Static/Picture/*']}

install_requires = \
['colorlog>=6.6.0,<7.0.0',
 'emoji>=1.7.0,<2.0.0',
 'fonttools>=4.31.2,<5.0.0',
 'httpx>=0.22.0,<0.23.0',
 'pillow>=9.1.0,<10.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'qrcode>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'dynamicrender',
    'version': '0.2.2',
    'description': 'BiliBili动态转图片',
    'long_description': None,
    'author': 'DMC',
    'author_email': 'lzxder@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
