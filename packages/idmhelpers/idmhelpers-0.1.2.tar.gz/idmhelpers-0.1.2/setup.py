# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idmhelpers']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=3,<4']

setup_kwargs = {
    'name': 'idmhelpers',
    'version': '0.1.2',
    'description': 'Helper library for common Databricks activities for Data Engineering, Delta Tables, Pipelines',
    'long_description': None,
    'author': 'divyavanmahajan',
    'author_email': 'divya.mahajan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
