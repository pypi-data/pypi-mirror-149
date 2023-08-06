# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monostate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'monostate',
    'version': '0.0.6',
    'description': 'Dependency-free monostate owner base class',
    'long_description': '# __monostate__\nDependency-free python package, providing monostate owner base class through implementation of the borg pattern\n\n[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)\n[![Build](https://github.com/w2sv/monostate/actions/workflows/build.yaml/badge.svg)](https://github.com/w2sv/monostate/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/w2sv/monostate/branch/master/graph/badge.svg?token=9EESND69PG)](https://codecov.io/gh/w2sv/monostate)\n![PyPI](https://img.shields.io/pypi/v/monostate)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n\n## Download\n```\npip install monostate\n```\n\n## Usage\n\n```python\nfrom monostate import MonoStateOwner\n\n\nclass MonoStateOwnerImplementation(MonoStateOwner):\n    def __init__(self, a, b):\n        super().__init__()\n        \n        # initialize instance as per usual...\n        \n        \n# Initialization of state:\nMonoStateOwnerImplementation(69, 420)\n\n# Instance retrieving:\ninstance = MonoStateOwnerImplementation.instance()\n```\n\n- Managing of multiple MonoStateOwner Subclasses with decoupled states supported\n\n## Author\nJanek Zangenberg\n\n## License\n[MIT](LICENSE)\n',
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
