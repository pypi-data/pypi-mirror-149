# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noo',
 'noo.cli',
 'noo.cli.components',
 'noo.impl',
 'noo.impl.core',
 'noo.impl.models',
 'noo.impl.packager',
 'noo.impl.packager.runners',
 'noo.impl.registry',
 'noo.impl.resolvers',
 'noo.impl.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tomli>=1.2.3,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['noo = noo:app']}

setup_kwargs = {
    'name': 'noo',
    'version': '2.0.0a1',
    'description': 'Easily create new projects.',
    'long_description': '# noo\n\nEasily create new projects.\n\n![Lint](https://github.com/nooproject/noo/actions/workflows/black.yml/badge.svg)\n\n## Installation\n\n```sh\npip install pynoo\n```\n\nor install from GitHub\n\n```sh\npip install git+https://github.com/nooproject/noo\n```\n\n## Contributing\n\nSee [contributing](./.github/CONTRIBUTING.md).\n\n## Basic Usage\n\n```sh\nnoo clone <name> <ref> - Clone a new project.\nnoo more <ref> - Modify the current project with a noofile.\n```\n\n## Documentation\n\nThe project documentation can be found on [our site](https://nooproject.dev).\n\nFor additional help you may find it useful to join our [Discord server](https://discord.gg/zbMBkC3849).\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nooproject/noo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
