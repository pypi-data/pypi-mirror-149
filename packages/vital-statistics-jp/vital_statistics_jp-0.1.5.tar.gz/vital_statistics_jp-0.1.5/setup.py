# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vital_statistics_jp']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0', 'pandas==1.3.5', 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'vital-statistics-jp',
    'version': '0.1.5',
    'description': 'vital statistics downloader',
    'long_description': '===================\nvital_statistics_jp\n===================\n\ndescription\n============\n\nThis module gets the vital statistics of Japan. Currently, it is possible to obtain monthly prompt data.\n\ninstall\n========\n\n.. code-block:: shell\n\n    pip install vital-statistics-jp\n\ncode example\n============\n\n.. code-block:: python\n\n    from vital-statistics-jp import read_prompt\n\n    stat_df = read_prompt()\n\n    print(stat_df)\n\n',
    'author': 'u-masao',
    'author_email': '4973920+u-masao@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/u-masao/vital_statistics_jp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
