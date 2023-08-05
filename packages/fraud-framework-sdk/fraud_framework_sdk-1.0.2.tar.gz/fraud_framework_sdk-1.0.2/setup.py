# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fraud_framework_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'fraud-framework-sdk',
    'version': '1.0.2',
    'description': 'Lightweight Python API to submit risk verification requests and other actions to the Fraud Framework.',
    'long_description': None,
    'author': 'mmcclelland1002',
    'author_email': 'mmcclelland@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
