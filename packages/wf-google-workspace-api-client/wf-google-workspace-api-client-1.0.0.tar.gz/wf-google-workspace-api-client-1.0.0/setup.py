# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wf_google_workspace_api_client',
 'wf_google_workspace_api_client.api',
 'wf_google_workspace_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'wf-google-workspace-api-client',
    'version': '1.0.0',
    'description': 'WF Google Workspace API client',
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
