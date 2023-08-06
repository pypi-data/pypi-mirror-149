# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect', 'connect.eaas.core']

package_data = \
{'': ['*']}

install_requires = \
['connect-openapi-client>=24.1,<25.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'connect-eaas-core',
    'version': '1.6.0',
    'description': 'Connect Eaas Core',
    'long_description': '',
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
