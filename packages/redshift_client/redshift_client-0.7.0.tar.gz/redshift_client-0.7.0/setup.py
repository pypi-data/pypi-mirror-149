# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redshift_client',
 'redshift_client.data_type',
 'redshift_client.schema',
 'redshift_client.sql_client',
 'redshift_client.table']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'fa-purity>=1.5.0,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'types-Deprecated>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'redshift-client',
    'version': '0.7.0',
    'description': 'Redshift client-SDK',
    'long_description': None,
    'author': 'Product Team',
    'author_email': 'development@fluidattacks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
