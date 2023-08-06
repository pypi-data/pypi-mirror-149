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
    'version': '0.1.1',
    'description': 'Extension of `argparse` to provide fast and customizable argument parsing.',
    'long_description': '# slap.core.cli\n\nExtension of [`argparse`][0] to provide fast and customizable argument parsing.\n\n  [0]: https://docs.python.org/3/library/argparse.html\n\n## Compatibility\n\nRequires Python 3.6 or higher.\n',
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
