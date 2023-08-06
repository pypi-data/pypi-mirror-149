# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['echoloader']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'opencv-python>=4.5.5.64,<5.0.0.0',
 'pydicom>=2.3.0,<3.0.0',
 'pynetdicom>=1.5.7,<2.0.0',
 'python-gdcm>=3.0.12,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'watchdog>=2.1.7,<3.0.0']

entry_points = \
{'console_scripts': ['echoloader = echoloader.watcher:main']}

setup_kwargs = {
    'name': 'echoloader',
    'version': '0.1.13',
    'description': '',
    'long_description': None,
    'author': 'mathias',
    'author_email': 'mathias@us2.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
