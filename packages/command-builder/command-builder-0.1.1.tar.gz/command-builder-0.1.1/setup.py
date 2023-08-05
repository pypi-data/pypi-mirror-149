# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['command_builder']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pipeline = ci_pipeline:main']}

setup_kwargs = {
    'name': 'command-builder',
    'version': '0.1.1',
    'description': 'Summary shell commands execution',
    'long_description': '# Command Builder\n\nCommand Builder is a library that manages the execution of shell commands, creating a summary of the executions. The objective is to facilitate the perception of errors.\n\n## Installation\n\n> You need Python 3.7 or above.\n\nFrom the terminal, enter:\n\n```bash\npip install command-builder\n```\n\n## Getting started\n\n> The examples refer to the newest version (0.1.0) of command-builder.\n\nFirst, let\'s init the command-builder:\n\n```python\nfrom command_builder.command_builder import CommandBuilder\n\ncommand_builder = CommandBuilder()\n\n```\n\nAdding commands:\n\n```python\ncommand_builder.add(name="ls", command=["ls", "-a"])\ncommand_builder.add(name="pwd", command=["pwd", "-o"])\n```\n\nRunning commands:\n\n```python\ncommand_builder.run()\n```\n\nOutput:\n\n```diff\n______________________________summary______________________________\n+ ls: commands succeeded\n- ERROR: pwd: commands failed\n```\n\n',
    'author': 'Guilherme Righetto',
    'author_email': 'guilhermerighetto02@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
