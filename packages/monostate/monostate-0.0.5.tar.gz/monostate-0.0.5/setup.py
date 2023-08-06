# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monostate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monostate',
    'version': '0.0.5',
    'description': 'Dependency-free monostate owner base class',
    'long_description': None,
    'author': 'w2sv',
    'author_email': 'zangenbergjanek@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/w2sv/monostate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
