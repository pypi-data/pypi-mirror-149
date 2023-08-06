# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['db_contrib_tool',
 'db_contrib_tool.evg_aware_bisect',
 'db_contrib_tool.setup_repro_env',
 'db_contrib_tool.symbolizer',
 'db_contrib_tool.utils']

package_data = \
{'': ['*'], 'db_contrib_tool': ['config/*']}

install_requires = \
['PyGithub==1.55',
 'PyYAML==6.0',
 'analytics-python==1.4.0',
 'distro==1.6.0',
 'evergreen.py==3.4.2',
 'oauthlib==3.1.1',
 'packaging>=21.3,<22.0',
 'pkce==1.0.3',
 'pydantic==1.8.2',
 'requests-oauthlib==1.3.0',
 'requests==2.26.0',
 'structlog==21.4.0']

entry_points = \
{'console_scripts': ['db-contrib-tool = db_contrib_tool.cli:main']}

setup_kwargs = {
    'name': 'db-contrib-tool',
    'version': '0.2.3',
    'description': "The `db-contrib-tool` - MongoDB's tool for contributors.",
    'long_description': "# db-contrib-tool\n\nThe `db-contrib-tool` - MongoDB's tools for contributors.\n\n## Table of contents\n\n- [Description](#description)\n- [Dependencies](#dependencies)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Contributor's Guide](#contributors-guide-local-development)\n    - [Install dependencies](#install-project-dependencies)\n    - [Run command line tool](#run-command-line-tool-local-development)\n    - [Run linters](#run-linters)\n    - [Run tests](#run-tests)\n    - [Pre-commit](#pre-commit)\n    - [Test pipx package](#test-pipx-package)\n    - [Versioning](#versioning)\n    - [Code Review](#code-review)\n    - [Deployment](#deployment)\n\n## Description\n\nThe command line tool with various subcommands:\n- `bisect` - performs an evergreen-aware git-bisect to find the 'last passing version' and 'first failing version' of mongo\n- `setup-repro-env`\n  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md)\n  - downloads and installs:\n    - particular MongoDB versions\n    - debug symbols\n    - artifacts (including resmoke, python scripts etc)\n    - python venv for resmoke, python scripts etc\n- `symbolize`\n  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/symbolizer/README.md)\n  - Symbolizes stacktraces from recent `mongod` and `mongos` binaries compiled in Evergreen, including patch builds, mainline builds, and release/production builds.\n  - Requires authenticating to an internal MongoDB symbol mapping service.\n\n## Dependencies\n\n- Python 3.7 or later (python3 from the [MongoDB Toolchain](https://github.com/10gen/toolchain-builder/blob/master/INSTALL.md) is highly recommended)\n\n## Installation\n\nMake sure [dependencies](#dependencies) are installed.\nUse [pipx](https://pypa.github.io/pipx/) to install db-contrib-tool that will be available globally on your machine:\n```bash\n$ python3 -m pip install pipx\n$ python3 -m pipx ensurepath\n```\n\nInstalling db-contrib-tool:\n```bash\n$ python3 -m pipx install db-contrib-tool\n```\n\nUpgrading db-contrib-tool:\n```bash\n$ python3 -m pipx upgrade db-contrib-tool\n```\n\n## Usage\n\nPrint out help message:\n```bash\n$ db-contrib-tool -h\n```\nMore information on the usage of `setup-repro-env` can be found [here](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md).\n\n## Contributor's Guide (local development)\n\n### Install project dependencies\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management.\n```bash\n$ poetry install\n```\n\n### Run command line tool (local development)\n\n```bash\n$ ENV=DEV poetry run db-contrib-tool -h\n```\n\n### Run linters\n\n```bash\n$ poetry run isort src tests\n$ poetry run black src tests\n```\n\n### Run tests\n\n```bash\n$ poetry run pytest\n```\n\n### Pre-commit\n\nThis project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run\nconfigured checks at git commit time.<br>\nTo enable pre-commit on your local repository run:\n```bash\n$ poetry run pre-commit install\n```\n\nTo run pre-commit manually:\n```bash\n$ poetry run pre-commit run\n```\n\n### Test pipx package\n\nPipx installation recommendations can be found in [installation](#installation) section.<br>\nThe tool can be installed via pipx from your local repo:\n```bash\n$ python3 -m pipx install /path/to/db-contrib-tool\n```\n\n### Versioning\n\nThis project uses [semver](https://semver.org/) for versioning.\nPlease include a description what is added for each new version in `CHANGELOG.md`.\n\n### Code Review\n\nPlease open a Github Pull Request for code review.\nThis project uses the [Evergreen Commit Queue](https://github.com/evergreen-ci/evergreen/wiki/Commit-Queue#pr).\nAdd a PR comment with `evergreen merge` to trigger a merge.\n\n### Deployment\n\nDeployment to pypi is automatically triggered on merges to main.\n",
    'author': 'STM team',
    'author_email': 'dev-prod-stm@10gen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/10gen/db-contrib-tool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
