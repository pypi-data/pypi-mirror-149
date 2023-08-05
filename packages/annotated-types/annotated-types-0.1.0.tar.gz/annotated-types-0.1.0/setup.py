# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annotated_types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'annotated-types',
    'version': '0.1.0',
    'description': 'Data only types to be used with PEP 593 annotations (typing.Annotated)',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
