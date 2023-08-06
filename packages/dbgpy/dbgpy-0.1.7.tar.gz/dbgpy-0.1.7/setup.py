# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbgpy']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.1,<22.0']

extras_require = \
{':python_version < "3.9"': ['astunparse>=1,<2']}

setup_kwargs = {
    'name': 'dbgpy',
    'version': '0.1.7',
    'description': "Python implementation of Rust's dbg! macro",
    'long_description': "# dbgpy\n\nDebug print inspired by Rust's `dbg!` macro.\n\nExample:\n\n```python\nfrom dbgpy import dbg\nimport numpy as np\n\narr = np.linspace(0, 10)\n\ndbg(arr.shape)\n```\n\nOutputs\n```\nmain.py:6: arr.shape = (50,)\n```\n\n",
    'author': 'Marcel Rød',
    'author_email': 'marcelroed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcelroed/dbgpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
