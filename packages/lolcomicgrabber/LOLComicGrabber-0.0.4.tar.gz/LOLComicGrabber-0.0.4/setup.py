# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lolcomicgrabber']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lolcomicgrabber',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'Shahriyar Shawon',
    'author_email': 'ShahriyarShawon321@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
