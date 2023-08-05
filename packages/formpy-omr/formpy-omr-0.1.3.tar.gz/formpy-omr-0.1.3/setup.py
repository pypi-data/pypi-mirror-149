# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formpy', 'formpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.2', 'numpy>=1.22.3,<2.0.0', 'opencv-contrib-python>=4.5.5,<5.0.0']

setup_kwargs = {
    'name': 'formpy-omr',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Ismail Mohammed',
    'author_email': 'ismailmo4@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
