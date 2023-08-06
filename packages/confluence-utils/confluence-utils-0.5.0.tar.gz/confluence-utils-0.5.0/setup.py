# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confluence_utils']

package_data = \
{'': ['*']}

install_requires = \
['atlassian-python-api>=3.21.0,<4.0.0',
 'click-log>=0.4.0,<0.5.0',
 'click-plugins>=1.1.1,<2.0.0',
 'click>=8,<9',
 'mistune>=2.0.2,<3.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['confluence = confluence_utils.cli:cli']}

setup_kwargs = {
    'name': 'confluence-utils',
    'version': '0.5.0',
    'description': '',
    'long_description': '# Confluence Utils\n\nCLI Utilities for Confluence.\n\n## Installation\n\n### System Requirements\n\n1. Python 3.7+\n\n### Install with `pipx` (recommended)\n\n1. Install [`pipx`](https://pypa.github.io/pipx/)\n1. Run `pipx install confluence-utils`\n\n### Install with `pip`:\n\n1. Run `pip install confluence-utils`\n\n## Usage\n\n### Commands\n\n#### `publish`\n\n```console\n$ confluence publish --help\nUsage: confluence publish [OPTIONS] PATH\n\nOptions:\n  --token TEXT  Confluence API Token. Optionally set with CONFLUENCE_TOKEN.\n                [required]\n  --space TEXT  Confluence Space. Optionally set with CONFLUENCE_SPACE.\n                [required]\n  --url TEXT    The URL to the Confluence API. Optionally set with\n                CONFLUENCE_URL.  [required]\n  --help        Show this message and exit.\n```\n',
    'author': 'Tevin Trout',
    'author_email': 'ttrout@bellese.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Bellese/confluence-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
