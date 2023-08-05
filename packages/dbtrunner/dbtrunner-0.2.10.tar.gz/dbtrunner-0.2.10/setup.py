# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbtrunner', 'dbtrunner.dbt.v1']

package_data = \
{'': ['*']}

install_requires = \
['google_api>=0.1.12,<0.2.0',
 'grpc-gateway-protoc-gen-openapiv2>=0.1.0,<0.2.0',
 'grpcio>=1.41.0,<2.0.0']

setup_kwargs = {
    'name': 'dbtrunner',
    'version': '0.2.10',
    'description': 'Python client stubs for invoking DBT runner calls',
    'long_description': '# dbtrunner\n\nPython package for easy implementation of remote DBT invocation using gRPC.\n',
    'author': 'Tom Collingwood',
    'author_email': 'tcollingwood@petsathome.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
