# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seito', 'seito.monad']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0',
 'aflowey>=0.1.1,<0.2.0',
 'aiohttp>=3.8.1,<4.0.0',
 'click==8.0.2',
 'fnmamoritai.py>=0.5.2,<0.6.0',
 'pampy>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'seito',
    'version': '0.1.2',
    'description': 'Functional helpers',
    'long_description': '# seito\n\nfunctional python (for learning)\nhttps://jerkos.github.io/seito/\n\nPython has some great functional features. The most notable ones are\ncomprehensions. However, when you start to chain function calls (or predicate\n or whatever), it becomes rapidly a pain.\n\nThere are 3 main modules:\n* option module: simplest implementation of the option monad \n``` python\nfrom seito import opt, none\n>>> opt(\'value\').or_else(\'new value\')\nvalue\n>>> opt(None).get() # same as none.get()\nTraceback (most recent call last):\n...\nValueError: Option is empty\n>>> o = opt([1, 2, 3]).map(print).or_else([])\n[1, 2, 3]\n>>> a = opt(\'optional option value\')\n>>> for i in a: print(i)\noptional option value\n\n>>> # forwarding value\n>>> class A(object):\n        def __init__(self, x):\n            self.x = x\n        def get_x(self):\n            return self.x\n        \n>>> opt(A(1)).get_x().or_else(0)\n1\n>>> opt(A(1)).get_y().or_else(0)\n0\n```\n* module dealing with json\n``` python\n>>> from seito.john import obj\n>>> i = obj({\'z-index\': 1000})\n>>> i.toto = [4, 5, 6]\n>>> i.stringify()\n\'{"z-index": 1000, "toto": [4, 5, 6]}\'\n```\n\n\nNotes: I found some python packages doing almost the same things. I did \nthis essentially to learn and wanted to keep it simple.\n',
    'author': 'Marc',
    'author_email': 'marc@synapse-medicine.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
