# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hybridmethods']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hybridmethods',
    'version': '0.1.1',
    'description': 'Library to create hybrids of class methods and instance methods',
    'long_description': '# hybridmethods\n\nA library for the creation of hybrid methods. Methods that can be called as either class methods or instance methods.\n\n## Usage\n\n```py\nfrom hybridmethods import *\n\n\nclass Test1:\n    @hybridmethod\n    def method(this):\n        if instance(this):  # Run when called as instance method\n            pass\n        else:  # Run when called as class method\n            pass\n    \n\nclass Test2:\n    @classmethod\n    def method(cls):\n        pass\n\n    @classmethod.instance\n    def _(self):\n        pass\n```\n',
    'author': 'Dense Reptile',
    'author_email': '80247368+DenseReptile@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
