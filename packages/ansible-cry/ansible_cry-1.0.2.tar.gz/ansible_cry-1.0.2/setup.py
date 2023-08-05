# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_cry']

package_data = \
{'': ['*']}

install_requires = \
['ansible', 'plumbum']

entry_points = \
{'console_scripts': ['cry = ansible_cry.cli:CRY.run']}

setup_kwargs = {
    'name': 'ansible-cry',
    'version': '1.0.2',
    'description': 'Encrypt and decrypt ansible-vault string/file: Perfect for external tools.',
    'long_description': "# CRY\nEncrypt and decrypt ansible-vault string/file perfect external tools\n\n```\nCRY me a river of encrypted data. Cry cry Cry.\n\nUtilisation:\n    cry [OPTIONS] [SUB_COMMAND [OPTIONS]] \n\nMeta-options:\n    -h, --help                        Print this message\n    --help-all                        Prints help messages of all sub-commands and quits\n    -v, --version                     Show version\n\nOptions:\n    --config VALEUR:ExistingFile      Filename with the vault password.; default: $HOME/.vault.pass\n    -d, --decrypt                     Encrypt by default, add -d to decrypt\n    --show-params                     Show parameters given to cry and exit.\n\nSub-commands:\n    file                              see 'cry file --help' for infos\n    string                            see 'cry string --help' for infos\n```\n\n```\nUtilisation:\n    cry file [OPTIONS] files...\n\nHidden-switches:\n    -h, --help              Print this message\n    --help-all              Prints help messages of all sub-commands and quits\n    -v, --version           Show version\n\nOptions:\n    -c, --show-context      Show the context around the string to decode\n```\n\n```\nUtilisation:\n    cry string [OPTIONS] strings...\n\nHidden-switches:\n    -h, --help         Print this message\n    --help-all         Prints help messages of all sub-commands and quits\n    -v, --version      Show version\n\nOptions:\n    -s, --stdin        Use stdin as source\n```",
    'author': 'Pierre-Yves Langlois',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylanglois/ansible-cry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
