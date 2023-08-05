# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['driftpy', 'driftpy.constants', 'driftpy.idl', 'driftpy.math']

package_data = \
{'': ['*']}

install_requires = \
['anchorpy>=0.8.0,<0.9.0',
 'requests>=2.27.1,<3.0.0',
 'solana>=0.21.0,<0.22.0',
 'types-requests>=2.27.8,<3.0.0']

setup_kwargs = {
    'name': 'driftpy',
    'version': '0.5.8',
    'description': 'A Python client for the Drift DEX',
    'long_description': '# DriftPy\n\n<div align="center">\n    <img src="https://camo.githubusercontent.com/d41b63c668d34e0ac5baba28a6fcff818da7b168752e511a605096dd9ba94039/68747470733a2f2f75706c6f6164732d73736c2e776562666c6f772e636f6d2f3631313538303033356164353962323034333765623032342f3631366639376134326635363337633435313764303139335f4c6f676f2532302831292532302831292e706e67" width="30%" height="30%">\n</div>\n\nDriftPy is the Python client for the [Drift](https://www.drift.trade/) protocol. It allows you to trade and fetch data from Drift using Python.\n\n[Read The Documentation](https://drift-labs.github.io/driftpy/)\n\n## Installation\n\n```\npip install driftpy\n```\n\nNote: requires Python >= 3.9.\n\n## Examples\n\n[Arbitrage Trading](https://github.com/0xbigz/driftpy-arb)\n\n[Querying and Visualization](https://gist.github.com/mcclurejt/b244d4ca8b0000ce5078ef8f60e937d9)\n\n## Development\n\n### Development Setup\n\nIf you want to contribute to DriftPy, follow these steps to get set up:\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Install dev dependencies:\n\n```sh\npoetry install\n\n```\n\n3. Install [nox-poetry](https://github.com/cjolowicz/nox-poetry) (note: do not use Poetry to install this, see [here](https://medium.com/@cjolowicz/nox-is-a-part-of-your-global-developer-environment-like-poetry-pre-commit-pyenv-or-pipx-1cdeba9198bd))\n4. Activate the poetry shell:\n\n```sh\npoetry shell\n\n```\n\n### Testing\n\n1. Run `make test`.\n2. Run `make lint`.\n\n### Building the docs\n\nRun `mkdocs serve` to build the docs and serve them locally.\n\n### Updating the embedded IDLs\n\nDriftPy ships with IDL files for the user\'s convenience. These live at `src/driftpy/idl` if you need to update them.\n\n### Releasing a new version of the package\n\n1. Make sure CHANGELOG.md is updated.\n2. Run `bumpversion major|minor|patch` to update the version number locally and create a tagged commit.\n3. Run `git push origin <version_number>` to push the tag to GitHub.\n4. After merging your PR on GitHub, create a new release at https://github.com/drift-labs/driftpy/releases.\n   The CI process will upload a new version of the package to PyPI.\n\n### Updating the `drift-core` subtree\n\n- This repo pulls in the main Drift repo using [git subtree](https://www.atlassian.com/git/tutorials/git-subtree).\n  Follow that linked tutorial if you want to see how it was done.\n\nThe short answer:\n`git subtree pull --prefix drift-core drift-protocol mainnet-beta --squash`\n',
    'author': 'Kevin Heavey',
    'author_email': 'kevinheavey123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drift-labs/driftpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
