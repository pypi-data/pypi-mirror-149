# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudreactor_api_client',
 'cloudreactor_api_client.api',
 'cloudreactor_api_client.api.alert_methods',
 'cloudreactor_api_client.api.email_notification_profiles',
 'cloudreactor_api_client.api.pagerduty_profiles',
 'cloudreactor_api_client.api.run_environments',
 'cloudreactor_api_client.api.task_executions',
 'cloudreactor_api_client.api.tasks',
 'cloudreactor_api_client.api.workflow_executions',
 'cloudreactor_api_client.api.workflow_task_instances',
 'cloudreactor_api_client.api.workflow_transitions',
 'cloudreactor_api_client.api.workflows',
 'cloudreactor_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'httpx>=0.15.4,<0.23.0', 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'cloudreactor-api-client',
    'version': '0.3.0.1',
    'description': 'A client library for accessing the CloudReactor API, which monitors and manages Tasks and Workflows.',
    'long_description': '# cloudreactor-python-api-client\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CloudReactor/cloudreactor-python-api-client/CI)](https://github.com/CloudReactor/cloudreactor-python-api-client/actions/workflows/ci.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/CloudReactor/cloudreactor-python-api-client)](https://app.codecov.io/github/CloudReactor/cloudreactor-python-api-client)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![PyPI](https://img.shields.io/pypi/v/cloudreactor-api-client)](https://pypi.org/project/cloudreactor-api-client/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudreactor-api-client)\n[![PyPI - License](https://img.shields.io/pypi/l/cloudreactor-api-client)](https://opensource.org/licenses/BSD-2-Clause)\n![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/CloudReactor/cloudreactor-python-api-client)\n\n\nPython client for the CloudReactor API\n\n## Overview\n\nThis python package allows python applications to programmatically\ncreate, monitor, and manage Tasks and Workflows in\n[CloudReactor](https://cloudreactor.io/). Most\nnotably, you can start and stop Tasks and Workflows by creating Task\nExecutions and Workflow Executions.\n\nSee the [CloudReactor landing page](https://www.cloudreactor.io/) to see the\nbenefits of monitoring and managing your tasks with CloudReactor.\n\n## Installation\n\nGet this package from PyPI:\n\n```bash\npip install cloudreactor_api_client\n```\n\n## Usage\n\nFirst, create a client:\n\n```python\nfrom cloudreactor_api_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.cloudreactor.io/api/v1",\n    token="YOUR_API_KEY")\n\n```\n\nTo start a Task, create a Task Execution:\n\n```python\nfrom cloudreactor_api_client.api.task_executions import (\n    task_executions_create\n)\nfrom cloudreactor_api_client.models import (\n    TaskExecution,\n    TaskExecutionStatus\n)\n\n# Identify the Task by name. Alternatively, you can specifiy the "uuid".\ntask_dict = {"name": "HappyTask"}\n\ntask_execution = TaskExecution.from_dict({\n    "task": task_dict,\n    "status": TaskExecutionStatus.MANUALLY_STARTED\n})\n\nresponse = task_executions_create.sync_detailed(client=client,\n    json_body=task_execution)\n\nparsed_task_execution = response.parsed\n\nprint(f"Task Execution {parsed_task_execution.uuid} started!")\n\n```\n\nMore details on how to use API clients in general (async mode, disabling SSL)\ncan be found in the generated [README](https://github.com/CloudReactor/cloudreactor-python-api-client/blob/master/cloudreactor-api-client/README-generated.md).\n\n\n## License\n\nThis software is licensed under the BSD 2-Clause License.\nSee `LICENSE` for details.\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://github.com/jtsay362"><img src="https://avatars0.githubusercontent.com/u/1079646?s=460&v=4?s=80" width="80px;" alt=""/><br /><sub><b>Jeff Tsay</b></sub></a><br /><a href="https://github.com/CloudReactor/cloudreactor-api-client/commits?author=jtsay362" title="Code">💻</a> <a href="https://github.com/CloudReactor/cloudreactor-procwrapper/commits?author=jtsay362" title="Documentation">📖</a> <a href="#infra-jtsay362" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-jtsay362" title="Maintenance">🚧</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n\n## Credits\n\nCode generated by [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)\n',
    'author': 'Jeff Tsay',
    'author_email': 'jeff@cloudreactor.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cloudreactor.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
