# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['callue']

package_data = \
{'': ['*']}

install_requires = \
['Paste>=3.5.0,<4.0.0',
 'bottle>=0.12.19,<0.13.0',
 'htmlmin>=0.1.12,<0.2.0',
 'jsmin>=3.0.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'rcssmin>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'callue',
    'version': '1.0.0',
    'description': 'A webserver preprocessor of sorts',
    'long_description': None,
    'author': 'Callum',
    'author_email': 'callum@jcwyt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
