# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymort', 'pymort.archive_2022_May_04_093934', 'pymort.pickled_tables']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'pymort',
    'version': '0.4.1',
    'description': '',
    'long_description': None,
    'author': 'Matthew Caseres',
    'author_email': 'matthewcaseres@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
