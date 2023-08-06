# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vital_statistics_jp']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0', 'pandas>=1.4.2,<2.0.0', 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'vital-statistics-jp',
    'version': '0.1.1',
    'description': 'vital statistics downloader',
    'long_description': None,
    'author': 'u-masao',
    'author_email': '4973920+u-masao@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
