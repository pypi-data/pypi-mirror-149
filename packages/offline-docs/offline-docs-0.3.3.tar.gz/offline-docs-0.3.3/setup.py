# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offline_docs']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0', 'urlpath>=1.2.0,<2.0.0', 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['offline-docs = offline_docs.cli:main']}

setup_kwargs = {
    'name': 'offline-docs',
    'version': '0.3.3',
    'description': 'CLI to quickly access docs of Python libraries, supporing offline usage.',
    'long_description': "# offline-docs\n\nQuick access to Python library docs, cached for offline availability.\n\n\n## Usage\n\n```\n$ offline-docs --help\n\n\nUsage: offline-docs [OPTIONS] COMMAND [ARGS]...\n\n  Quick access to Python library docs, cached for offline availability.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  clean   Remove all downloaded docs from local cache.\n  python  Open docs for the current Python version in browser.\n```\n\n\n## Related Projects\n\nAn overview of similar projects, and how `office-docs` is different:\n\n### Zeal\n\nMission statement, according to [zealdocs.org](https://zealdocs.org/):\n\n> *Zeal is an offline documentation browser for software developers.*\n\nCompared to zeal, `offline-docs`: \n* provides a command-line interface,\n* shows docs in the system's default browser,\n* matches the versions of docs to the installed versions.\n\n## Roadmap\n\nThis section gives an outlook on how `offline-docs` could develop in the future. \n\n* Download docs from [readthedocs.org](https://readthedocs.org).\n",
    'author': 'top-on',
    'author_email': 'top-on@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
