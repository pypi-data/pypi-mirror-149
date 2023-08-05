# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xist']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xist',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Nikhil Rao',
    'author_email': 'nikhil@xist.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
