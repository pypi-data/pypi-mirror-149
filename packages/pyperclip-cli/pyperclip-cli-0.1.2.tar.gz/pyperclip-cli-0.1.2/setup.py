# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyperclip_cli']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['pyperclip = pyperclip_cli.cli:main']}

setup_kwargs = {
    'name': 'pyperclip-cli',
    'version': '0.1.2',
    'description': 'Pyperclip CLI - cross-platform clipboard utility',
    'long_description': '# git pp\n\nPyperclip CLI - cross-platform clipboard utility\n\n- [git pp](#git-pp)\n  - [Features](#features)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Usage](#usage)\n  - [Develop](#develop)\n\n## Features\n\n- Copy and paste from stdin / stdout or files\n- Cross-platform\n\n## Installation\n\nCurrently only handles plaintext.\n\nOn Windows, no additional modules are needed.\n\nOn Mac, this module makes use of the pbcopy and pbpaste commands, which should come with the os.\n\nOn Linux, this module makes use of the xclip or xsel commands, which should come with the os. Otherwise run "sudo apt-get install xclip" or "sudo apt-get install xsel" (Note: xsel does not always seem to work.)\n\nOtherwise on Linux, you will need the gtk or PyQt4 modules installed.\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install pyperclip-cli\n```\n\n### [pip](https://pypi.org/project/pyperclip-cli/)\n```\n$ pip install pyperclip-cli\n```\n\n\n## Usage\n\n```\n$ pyperclip --help\n\nusage: pyperclip [-h] [-f FILE] [-o OUT] [ACTION]\n\nPyperclip CLI\n\npositional arguments:\n  ACTION                copy or paste (default: copy)\n\noptions:\n  -h, --help            show this help message and exit\n  -f FILE, --file FILE  Copy the content of the file (default: <_io.TextIOWrapper name=\'<stdin>\' mode=\'r\' encoding=\'utf-8\'>)\n  -o OUT, --out OUT     Paste to file (default: <_io.TextIOWrapper name=\'<stdout>\' mode=\'w\' encoding=\'utf-8\'>)\n```\n\n## Develop\n```\n$ git clone https://github.com/tddschn/pyperclip-cli.git\n$ cd pyperclip-cli\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/pyperclip-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
