# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'slap.core.cli',
    'version': '0.1.3',
    'description': 'Extension of `argparse` to provide fast and customizable argument parsing.',
    'long_description': '# slap.core.cli\n\nExtension of [`argparse`][0] to provide fast and customizable argument parsing.\n\n  [0]: https://docs.python.org/3/library/argparse.html\n\n## Usage\n\n```py\nimport argparse\nfrom typing import Any, Optional\n\nfrom slap.core.cli import CliApp, Command\n\n\nclass HelloCommand(Command):\n    def init_parser(self, parser: argparse.ArgumentParser) -> None:\n        parser.add_argument("name")\n\n    def execute(self, args: Any) -> Optional[int]:\n        print(f"Hello, {args.name}!")\n\n\napp = CliApp("minimal", "0.1.0")\napp.add_command("hello", HelloCommand())\napp.run()\n```\n\nGives you the following CLI:\n\n```\n$ python examples/minimal.py\nusage: minimal [-h] [-v] [--version] [{hello}] ...\n\npositional arguments:\n  {hello}        The subcommand to execute.\n  ...            Arguments for the subcommand.\n\noptions:\n  -h, --help     show this help message and exit\n  -v, --verbose  Increase the verbosity level.\n  --version      show program\'s version number and exit\n\nsubcommands:\n  hello\n```\n\n## Compatibility\n\nRequires Python 3.6 or higher.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
