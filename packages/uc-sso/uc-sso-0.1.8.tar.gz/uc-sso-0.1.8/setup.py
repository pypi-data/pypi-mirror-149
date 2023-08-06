# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uc_sso']

package_data = \
{'': ['*']}

install_requires = \
['html-table-parser-python3>=0.2.0,<0.3.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'uc-sso',
    'version': '0.1.8',
    'description': "A helper for interacting locally with services that are protected by UC Chile's SSO.",
    'long_description': '# UC SSO Helper 🔐\n\nA python library for easily authenticating to services protected by UC Chile\'s SSO system. Note this is meant for accessing services locally (i.e. not on a web app or user-facing system).\n\n## Installation\n\nThe library is available on PyPi:\n\n```shell\n$ pip install uc-sso\n```\n\n## Usage\n\nThe library exposes two main functions:\n\n- `get_ticket(username, password, service_url)`: To get a service ticket and an authenticated service URL given a username and password.\n- `get_user_info(username, password)`: To get SSO stored user attributes.\n\nThe library is typed and the [code](https://github.com/agucova/sso-uc/blob/main/uc_sso_helper/main.py) is relatively short and documented.\n\n### Seguimiento Curricular\n\nA minimal example to place an authenticated GET request to UC Chile\'s "Seguimiento Curricular" service:\n\n\n```python\nimport requests\n\nfrom uc_sso import get_ticket\n\nticket = get_ticket("example_username", "example_password", "https://seguimientocurricular.uc.cl/")\nrequests.get(ticket.service_url).text\n```\n\n### Getting user info\n\n```python\nfrom uc_sso import get_user_info\nprint(get_user_info("example_username", "example_password"))\n\n>>> {\n "full_name": "AGUSTIN COVARRUBIAS XXXXXX",\n "given_name": "AGUSTÍN",\n "surnames": "COVARRUBIAS XXXXXX",\n "first_last_name": "COVARRUBIAS",\n "second_last_name": "XXXXXX",\n "mail": "XXXXXX@uc.cl",\n "email_type": "gmail",\n "username": "XXXXXXX"\n "run": "XXXXXXX-0",\n "alternate_emails": ["XXXXXX@puc.cl"],\n "user_category": "Alumno",\n "user_type": "1"\n}\n```',
    'author': 'Agustín Covarrubias',
    'author_email': 'agucova@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agucova/sso-uc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
