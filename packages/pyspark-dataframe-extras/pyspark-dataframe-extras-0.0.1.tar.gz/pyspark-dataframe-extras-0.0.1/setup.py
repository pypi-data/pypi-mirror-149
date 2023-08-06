# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyspark_dataframe_extras', 'pyspark_dataframe_extras.common']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyspark-dataframe-extras',
    'version': '0.0.1',
    'description': 'Utility functions for PySpark',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
