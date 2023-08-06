# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wf_airtable_api_client', 'wf_airtable_api_client.api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'wf-airtable-api-schema>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'wf-airtable-api-client',
    'version': '1.3.0',
    'description': 'WF Airtable API client',
    'long_description': None,
    'author': 'Benjamin Jaffe-Talberg',
    'author_email': 'ben.talberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
