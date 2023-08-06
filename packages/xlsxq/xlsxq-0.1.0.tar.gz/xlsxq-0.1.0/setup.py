# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xlsxq']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0']

entry_points = \
{'console_scripts': ['xlsxq = xlsxq:main']}

setup_kwargs = {
    'name': 'xlsxq',
    'version': '0.1.0',
    'description': 'xlsxq is a lightweight and flexible command-line .xlsx processor.',
    'long_description': None,
    'author': 'kumarstack55',
    'author_email': 'kumarstack55@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
