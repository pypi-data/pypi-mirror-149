# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongolite',
 'pymongolite.backend',
 'pymongolite.backend.execution_engine',
 'pymongolite.backend.indexing_engine',
 'pymongolite.backend.storage_engine']

package_data = \
{'': ['*']}

install_requires = \
['blist>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'pymongolite',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'yehoyada',
    'author_email': 'yehoyada.sht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
