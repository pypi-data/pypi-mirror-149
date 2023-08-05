# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idmhelpers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'idmhelpers',
    'version': '0.1.0',
    'description': 'Helper library for common Databricks activities for Data Engineering, Delta Tables, Pipelines',
    'long_description': None,
    'author': 'divyavanmahajan',
    'author_email': 'divya.mahajan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
