# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudwatcher']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'boto3>=1.21.46,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pytz>=2022.1,<2023.0',
 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['cloudwatcher = cloudwatcher.__main__:main']}

setup_kwargs = {
    'name': 'cloudwatcher',
    'version': '0.0.6',
    'description': 'A tool for monitoring AWS CloudWatch metrics',
    'long_description': None,
    'author': 'Michal Stolarczyk',
    'author_email': 'stolarczyk.michal93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
