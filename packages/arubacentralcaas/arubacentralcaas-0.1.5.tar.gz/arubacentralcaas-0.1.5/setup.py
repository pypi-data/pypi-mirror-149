# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arubacentralcaas',
 'arubacentralcaas.config',
 'arubacentralcaas.deprecated',
 'arubacentralcaas.deprecated.cookie_version',
 'arubacentralcaas.deprecated.lib',
 'arubacentralcaas.model',
 'arubacentralcaas.tests',
 'arubacentralcaas.views']

package_data = \
{'': ['*'],
 'arubacentralcaas': ['.cache/*', 'images/*', 'samples/*'],
 'arubacentralcaas.tests': ['resources/*']}

install_requires = \
['ipaddress>=1.0.23,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pycentral>=0.0.3,<0.0.4',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=12.3.0,<13.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['caas = arubacentralcaas.app:app']}

setup_kwargs = {
    'name': 'arubacentralcaas',
    'version': '0.1.5',
    'description': 'Aruba Central CaaS API CLI',
    'long_description': None,
    'author': 'Michael Rose Jr.',
    'author_email': 'michael@michaelrosejr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
