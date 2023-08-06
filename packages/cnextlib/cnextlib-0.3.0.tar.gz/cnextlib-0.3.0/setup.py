# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnextlib', 'cnextlib.libs', 'cnextlib.tests']

package_data = \
{'': ['*'],
 'cnextlib.tests': ['.ipynb_checkpoints/*',
                    'data/housing_data/*',
                    'data/machine-simulation/*']}

setup_kwargs = {
    'name': 'cnextlib',
    'version': '0.3.0',
    'description': 'cyc libraries for cyc-next-app',
    'long_description': None,
    'author': 'cycai company',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
