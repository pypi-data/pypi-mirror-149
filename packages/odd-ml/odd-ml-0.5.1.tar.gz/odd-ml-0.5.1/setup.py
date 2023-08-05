# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_ml', 'odd_ml.domain', 'odd_ml.utils']

package_data = \
{'': ['*']}

install_requires = \
['fastparquet>=0.8.1,<0.9.0',
 'pandas>=1.4.2,<2.0.0',
 'prettytable>=3.2.0,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0',
 's3fs>=2022.3.0,<2023.0.0',
 's3path>=0.3.4,<0.4.0']

setup_kwargs = {
    'name': 'odd-ml',
    'version': '0.5.1',
    'description': 'SDK for working with pipelines from notebooks',
    'long_description': None,
    'author': 'Pavel Makarichev',
    'author_email': 'vixtir90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.12,<4.0.0',
}


setup(**setup_kwargs)
