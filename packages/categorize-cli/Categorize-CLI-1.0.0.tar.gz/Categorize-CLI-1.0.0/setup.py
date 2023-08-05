# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Categorize_CLI',
 'Categorize_CLI.commands',
 'Categorize_CLI.common',
 'Categorize_CLI.services']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0', 'colorama>=0.4.4,<0.5.0', 'progress>=1.6,<2.0']

entry_points = \
{'console_scripts': ['Categorize = src.Categorize_CLI.__main__:main']}

setup_kwargs = {
    'name': 'categorize-cli',
    'version': '1.0.0',
    'description': 'Categorize-CLI is a command-line-tool made to help you categorize/organize files in a given directory',
    'long_description': '<div align="center">\n<h1>Categorize-CLI</h1>\n<a href="https://github.com/Rohith-JN/Categorize-CLI/blob/main/LICENSE.txt">\n  <img src="https://img.shields.io/github/license/Rohith-JN/Categorize-CLI?color=blue&style=flat-square" title="License">\n</a>\n<a href="https://pypi.org/project/Categorize-CLI/">\n  <img src="https://img.shields.io/pypi/v/Categorize-CLI?color=blue&style=flat-square" title="PyPI Version">\n</a>\n<p>A command-line-tool to help you organize files in a given directory\n</p>\n\n</div>\n\n---\n\n## Categorize-CLI v1.0.0\n\nA new update aimed to simplify the command-line-interface while increasing functionality\n\n- [View the changelog](https://github.com/Rohith-JN/Categorize-CLI/blob/main/CHANGELOG.md) for all the new features!\n\n## Usage\n\n### Extensions:\nThis command will organize the files based on the specified extension type (ex: image, audio, video) in the working directory\n\n```\nCategorize ext -t [command]\n```\n\n```\nCategorize ext --type [command]\n```\n\nTo organize all files based on extension (ex: .jpeg, .txt) use the `--all` flag\n\n```\nCategorize ext --all\n```\nCommands:\n\n```\n[text, image, audio, video, word, powerpoint, excel, access, executables, pdf, archives, documents, media, safe]\n```\n\n### Keyword:\nThis command will organize the files based on the specified keyword present in the file names in the working directory\n\n```\nCategorize key -k [command]\n```\n```\nCategorize key --keyword [command]\n```\n\n### Year-created:\n\nThis command will organize files based on year created in the working directory\n\n```\nCategorize year\n```\n\n\n### Other\nIf you want to organize files belonging to another directory then you can just specify the path using this option `-p` or `--path`\n\n```\nCategorize [command] --path [command]\n```\n\nIf you want to view the full output you can use the verbose flag `-v` or `--verbose`\n\n```\nCategorize [command] --verbose\n```\n\nCommand line interface\n\n```\nUsage: Categorize [OPTIONS] COMMAND [ARGS]...\n\n  Categorize files based on different categories\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  ext   Organize files based on specified extension (ex: image, video)\n  key   Organize files based on specified keyword\n  year  Organize files based on year created\n```',
    'author': 'Rohith Nambiar',
    'author_email': 'rohithnambiar04@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rohith-JN/Categorize-CLI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
