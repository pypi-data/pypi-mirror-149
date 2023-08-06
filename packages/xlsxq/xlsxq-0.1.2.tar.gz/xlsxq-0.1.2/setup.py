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
    'version': '0.1.2',
    'description': 'xlsxq is a lightweight and flexible command-line .xlsx processor.',
    'long_description': "# xlsxq\n\nxlsxq is a lightweight and flexible command-line .xlsx processor.\n\n# Usage\n\nThis is a beta version and specifications are subject to change.\n\n```bash\n# Show help message and exit.\nxlsxq -h\n\n# List worksheets.\nxlsxq sheet list --infile infile.xlsx --output json\n\n# Show range values.\nxlsxq range show --infile infile.xlsx --sheet 'Sheet1' --range 'A1:B3' --output json\n\n# Show range values in tab-delimited format.\nxlsxq range show --infile infile.xlsx --sheet 'Sheet1' --range 'A1:B3' --output tsv\n```\n\n# Requirements\n\n* Python 3.9+\n\n# Installation\n\n```bash\npip install -U xlsxq\n```\n\n# TODO\n\n* Write docs\n",
    'author': 'kumarstack55',
    'author_email': 'kumarstack55@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kumarstack55/xlsxq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
