# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['agoradesk_py']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.1,<2.0.0', 'httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'agoradesk-py',
    'version': '0.3.1',
    'description': 'Python Interface for Agoradesk.com and LocalMonero.co API',
    'long_description': '# agoradesk_py\nPython interface for [AgoraDesk.com/LocalMonero.co API](https://agoradesk.com/api-docs/v1).\n\nThis is currently not a complete implementation of the Agoradesk API.\n\nThe following API calls are currently **not** supported.\n- Image uploading in chat\n\n\n**I offer no warranty of any kind -- use this at your own risk!**\n\n*I am not associated with AgoraDesk.com or LocalMonero.co.*\n\n# Requirements:\nThe two main requirements are [httpx](https://www.python-httpx.org/) and [arrow](https://arrow.readthedocs.io/en/latest/).\nI am using [Poetry](https://python-poetry.org/docs/) with this project to keep track of dependencies / requirements.\n\n# Install\n\n`pip install agoradesk_py`\n\n# How to Use\nThis is an example about how you can use the library\n\n```\n#!/usr/bin/env python3\n\nfrom agoradesk_py.agoradesk import AgoraDesk\n\napi_key = <YourAPIKey>\n\napi = AgoraDesk(api_key)\n\n# Get information about all released trades\napi_response = api.dashboard_released()\n\nif api_response["success"]:\n    trades = api_response["response"]["data"]["contact_list"]\n\n    for trade in trades:\n        trade_data = trade["data"]\n        print(\n            f"Traded "\n            f"{trade_data[\'amount_xmr\']} XMR with a fee of {trade_data[\'fee_xmr\']} XMR "\n            f"for {trade_data[\'amount\']} {trade_data[\'currency\']} "\n            f"on {trade_data[\'released_at\']}"\n        )\n\nelse:\n     print(f"Error: {api_response[\'response\'][\'error\']}")\n\n```\n\n# Running Tests\n**Please be aware of the unauthenticated API requests limit of 20 req/h**\n\nTests are split into Unit tests and integration tests.\n\nTo prepare to run any tests:\n1) Clone this repository to your computer.\n2) Install [Poetry](https://python-poetry.org/docs/)\n3) Install all dependencies / requirements for agoradesk_py using the command `poetry install` in the project directory.\n\n## Unit Tests\nUnit tests do not communicate with LocalMonero / AgoraDesk and are executed entirely locally.\n\nRunning all unit tests with coverage report is as easy as using the command\n`poetry run pytest --cov-report term-missing tests/unit/` in the project directory,\n\n## Integration Tests\n\nIntegration tests communicate with the actual LocalMonero / AgoraDesk production APIs and the tests depend on\nthe two following environment variables being set to the api_keys of two testing accounts at LocalMonero.co.\n* api_key\n* api_key2\n\nPlease be aware that:\n* LocalMonero.co or AgoraDesk.com are not currently providing a testing setup and all testes are running in their production environment.\n* For some tests to run successfully the account for `api_key2` needs to have a balance of currently about 0.1 XMR\n* The two testing account need to be set to trust each other for all the tests to be successful.\n\nTo run the integration tests use the command `poetry run pytest tests/integration/`\n\n# Contribute\nDo you have an idea or found a bug in agoradesk_py? Please file an issue and/or submit a pull request! :)\n\nSource code is currently on [Codeberg](https://codeberg.org) at https://codeberg.org/MarvinsCryptoTools/agoradesk_py\n\n## Support\nIf you like the API and want to support me you can do so with\nMonero:\n    88NszkQU9qsafT9obFaDZSi7RvHSM76exJ1vvgVShTwM4HjvLr7XjJ7jDkFGnxr3UsDXLgT5t569N6uB7Gn4znjAFjUuN1q\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/MarvinsCryptoTools/agoradesk_py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
