# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_attire_schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'py-attire-schema',
    'version': '1.1.0',
    'description': 'Base logging schema used by attire logger projects',
    'long_description': None,
    'author': 'jamesgeraghty',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SecurityRiskAdvisors/py-attire-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
