# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_utils', 'aiogram_utils.filters', 'aiogram_utils.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiogram>=2.20,<3.0',
 'mongoengine>=0.24.1,<0.25.0',
 'ujson>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'aiogram-utils',
    'version': '0.1.4',
    'description': 'Misc utils for aiogram',
    'long_description': '# TODO',
    'author': 'LDmitriy7',
    'author_email': 'ldm.work2019@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LDmitriy7/aiogram_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
