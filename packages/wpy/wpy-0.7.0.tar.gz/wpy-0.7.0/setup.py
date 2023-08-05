# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wpy',
 'wpy.app',
 'wpy.cli',
 'wpy.common',
 'wpy.completion',
 'wpy.process',
 'wpy.shell']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wpy',
    'version': '0.7.0',
    'description': 'a library for python Developer',
    'long_description': None,
    'author': 'wxnacy',
    'author_email': 'wxnacy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
