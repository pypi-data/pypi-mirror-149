# db-contrib-tool

The `db-contrib-tool` - MongoDB's tools for contributors.

## Table of contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributor's Guide](#contributors-guide-local-development)
    - [Install dependencies](#install-project-dependencies)
    - [Run command line tool](#run-command-line-tool-local-development)
    - [Run linters](#run-linters)
    - [Run tests](#run-tests)
    - [Pre-commit](#pre-commit)
    - [Test pipx package](#test-pipx-package)
    - [Versioning](#versioning)
    - [Code Review](#code-review)
    - [Deployment](#deployment)

## Description

The command line tool with various subcommands:
- `bisect` - performs an evergreen-aware git-bisect to find the 'last passing version' and 'first failing version' of mongo
- `setup-repro-env`
  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md)
  - downloads and installs:
    - particular MongoDB versions
    - debug symbols
    - artifacts (including resmoke, python scripts etc)
    - python venv for resmoke, python scripts etc
- `symbolize`
  - [README.md](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/symbolizer/README.md)
  - Symbolizes stacktraces from recent `mongod` and `mongos` binaries compiled in Evergreen, including patch builds, mainline builds, and release/production builds.
  - Requires authenticating to an internal MongoDB symbol mapping service.

## Dependencies

- Python 3.7 or later (python3 from the [MongoDB Toolchain](https://github.com/10gen/toolchain-builder/blob/master/INSTALL.md) is highly recommended)

## Installation

Make sure [dependencies](#dependencies) are installed.
Use [pipx](https://pypa.github.io/pipx/) to install db-contrib-tool that will be available globally on your machine:
```bash
$ python3 -m pip install pipx
$ python3 -m pipx ensurepath
```

Installing db-contrib-tool:
```bash
$ python3 -m pipx install db-contrib-tool
```

Upgrading db-contrib-tool:
```bash
$ python3 -m pipx upgrade db-contrib-tool
```

## Usage

Print out help message:
```bash
$ db-contrib-tool -h
```
More information on the usage of `setup-repro-env` can be found [here](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/setup_repro_env/README.md).

## Contributor's Guide (local development)

### Install project dependencies

This project uses [poetry](https://python-poetry.org/) for dependency management.
```bash
$ poetry install
```

### Run command line tool (local development)

```bash
$ ENV=DEV poetry run db-contrib-tool -h
```

### Run linters

```bash
$ poetry run isort src tests
$ poetry run black src tests
```

### Run tests

```bash
$ poetry run pytest
```

### Pre-commit

This project has [pre-commit](https://pre-commit.com/) configured. Pre-commit will run
configured checks at git commit time.<br>
To enable pre-commit on your local repository run:
```bash
$ poetry run pre-commit install
```

To run pre-commit manually:
```bash
$ poetry run pre-commit run
```

### Test pipx package

Pipx installation recommendations can be found in [installation](#installation) section.<br>
The tool can be installed via pipx from your local repo:
```bash
$ python3 -m pipx install /path/to/db-contrib-tool
```

### Versioning

This project uses [semver](https://semver.org/) for versioning.
Please include a description what is added for each new version in `CHANGELOG.md`.

### Code Review

Please open a Github Pull Request for code review.
This project uses the [Evergreen Commit Queue](https://github.com/evergreen-ci/evergreen/wiki/Commit-Queue#pr).
Add a PR comment with `evergreen merge` to trigger a merge.

### Deployment

Deployment to pypi is automatically triggered on merges to main.
