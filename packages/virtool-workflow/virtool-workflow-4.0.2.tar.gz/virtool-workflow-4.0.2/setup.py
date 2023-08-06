# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixtures',
 'fixtures.tests',
 'virtool_workflow',
 'virtool_workflow.analysis',
 'virtool_workflow.api',
 'virtool_workflow.data_model',
 'virtool_workflow.execution',
 'virtool_workflow.runtime',
 'virtool_workflow.testing']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.0,<6.0.0',
 'aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aioredis==1.3.1',
 'click>=8.0.0,<9.0.0',
 'sentry-sdk>=1.5.7,<2.0.0',
 'virtool-core>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['run-workflow = virtool_workflow.cli:cli_main']}

setup_kwargs = {
    'name': 'virtool-workflow',
    'version': '4.0.2',
    'description': 'A framework for developing bioinformatics workflows for Virtool.',
    'long_description': '# Virtool Workflow\n\n![Tests](https://github.com/virtool/virtool-workflow/workflows/Tests/badge.svg?branch=master)\n[![PyPI version](https://badge.fury.io/py/virtool-workflow.svg)](https://badge.fury.io/py/virtool-workflow)\n\nA framework for developing bioinformatic workflows in Python.\n\n```python\nfrom virtool_workflow import startup, step, cleanup\n\n@startup\ndef startup_function():\n    ...\n\n@step \ndef step_function():\n    ...\n\n@step\ndef step_function_2():\n    ...\n\n@cleanup\ndef cleanup_function():\n    ...\n```\n\n* [Documentation](https://workflow.virtool.ca)\n* [Website](https://www.virtool.ca/)\n\n## Contributing \n\n### Commits\n\nAll commits must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0) specification.\n\nThese standardized commit messages are used to automatically publish releases using [`semantic-release`](https://semantic-release.gitbook.io/semantic-release)\nafter commits are merged to `main` from successful PRs.\n\n**Example**\n\n```text\nfeat: add API support for assigning labels to existing samples\n```\n\nDescriptive bodies and footers are required where necessary to describe the impact of the commit. Use bullets where appropriate.\n\nAdditional Requirements\n1. **Write in the imperative**. For example, _"fix bug"_, not _"fixed bug"_ or _"fixes bug"_.\n2. **Don\'t refer to issues or code reviews**. For example, don\'t write something like this: _"make style changes requested in review"_.\nInstead, _"update styles to improve accessibility"_.\n3. **Commits are not your personal journal**. For example, don\'t write something like this: _"got server running again"_\nor _"oops. fixed my code smell"_.\n\nFrom Tim Pope: [A Note About Git Commit Messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)\n',
    'author': 'Ian Boyes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/virtool/virtool-workflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
