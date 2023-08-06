# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cognito_pyauth']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2.0,<3.0',
 'boto3>=1.0,<2.0',
 'fastapi>=0.75.0,<1.0',
 'pydantic>=1.0,<2.0',
 'requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'cognito-pyauth',
    'version': '1.3.2',
    'description': '',
    'long_description': '# cognito-pyauth\n\n',
    'author': 'fuuga',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
