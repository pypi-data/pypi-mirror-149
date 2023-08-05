# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nordigen', 'nordigen.api', 'nordigen.types', 'nordigen.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'nordigen',
    'version': '1.1.0',
    'description': 'Python client for Nordigen API',
    'long_description': '# Nordigen Python\n\nThis is official Python client library for [Nordigen](https://nordigen.com/en) API\n\nFor a full list of endpoints and arguments, see the [docs](https://nordigen.com/en/account_information_documenation/api-documention/overview/).\n\nBefore starting to use API you will need to create a new secret and get your `SECRET_ID` and `SECRET_KEY` from the [Nordigen\'s Open Banking Portal](https://ob.nordigen.com/user-secrets/).\n\n## Requirements\n\n* Python >= 3.8\n\n\n## Installation\n\nInstall library via pip package manager:\n\n```\npip install nordigen\n```\n\n## Example application\n\nExample code can be found in `main.py` file and Flask application can be found in the `example` directory\n\n## Quickstart\n\n\n```python\nfrom uuid import uuid4\n\nfrom nordigen import NordigenClient\n\n# initialize Nordigen client and pass SECRET_ID and SECRET_KEY\nclient = NordigenClient(\n    secret_id="SECRET_ID",\n    secret_key="SECRET_KEY"\n)\n\n# Create new access and refresh token\n# Parameters can be loaded from .env or passed as a string\n# Note: access_token is automatically injected to other requests after you successfully obtain it\ntoken_data = client.generate_token()\n\n# Use existing token\nclient.token = "YOUR_TOKEN"\n\n# Exchange refresh token for new access token\nnew_token = client.exchange_token(token_data["refresh"])\n\n# Get institution id by bank name and country\ninstitution_id = client.institution.get_institution_id_by_name(\n    country="LV",\n    institution="Revolut"\n)\n\n# Get all institution by providing country code in ISO 3166 format\ninstitutions = client.institution.get_institutions("LV")\n\n# Initialize bank session\ninit = client.initialize_session(\n    # institution id\n    institution_id=institution_id,\n    # redirect url after successful authentication\n    redirect_uri="https://nordigen.com",\n    # additional layer of unique ID defined by you\n    reference_id=str(uuid4())\n)\n\n# Get requisition_id and link to initiate authorization process with a bank\nlink = init.link # bank authorization link\nrequisition_id = init.requisition_id\n```\n\nAfter successful authorization with a bank you can fetch your data (details, balances, transactions)\n\n---\n\n## Fetching account metadata, balances, details and transactions\n\n```python\n\n# Get account id after you have completed authorization with a bank\n# requisition_id can be gathered from initialize_session response\naccounts = client.requisition.get_requisition_by_id(\n    requisition_id=init.requisition_id\n)\n\n# Get account id from the list.\naccount_id = accounts["accounts"][0]\n\n# Create account instance and provide your account id from previous step\naccount = client.account_api(id=account_id)\n\n# Fetch account metadata\nmeta_data = account.get_metadata()\n# Fetch details\ndetails = account.get_details()\n# Fetch balances\nbalances = account.get_balances()\n# Fetch transactions\ntransactions = account.get_transactions()\n# Filter transactions by specific date range\ntransactions = account.get_transactions(date_from="2021-12-01", date_to="2022-01-21")\n\n```\n\n## Support\n\nFor any inquiries please contact support at [support@nordigen.com](support@nordigen.com) or create an issue in repository.\n',
    'author': 'Nordigen Solutions',
    'author_email': 'support@nordigen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nordigen/nordigen-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
