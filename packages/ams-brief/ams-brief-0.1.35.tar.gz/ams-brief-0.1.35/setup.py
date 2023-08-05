# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ams_brief']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'fpdf>=1.7.2,<2.0.0', 'imagesize>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['ams-brief = ams_brief.console:main']}

setup_kwargs = {
    'name': 'ams-brief',
    'version': '0.1.35',
    'description': '',
    'long_description': None,
    'author': 'Lucas',
    'author_email': 'lucas@animotions.be',
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
