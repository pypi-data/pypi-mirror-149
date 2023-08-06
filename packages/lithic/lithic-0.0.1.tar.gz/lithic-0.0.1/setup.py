# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lithic', 'lithic.resources', 'lithic.types']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0',
 'typing-extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'lithic',
    'version': '0.0.1',
    'description': 'Client library for the lithic API',
    'long_description': None,
    'author': 'Lithic',
    'author_email': 'sdk-feedback@lithic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lithic-com/lithic-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
