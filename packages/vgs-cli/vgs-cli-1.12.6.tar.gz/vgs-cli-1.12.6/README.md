# VGS CLI
[![CircleCI](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=dff66120c964e4fbf51dcf059b03746910d0449d)](https://circleci.com/gh/verygoodsecurity/vgs-cli/tree/master)

Command Line Tool for programmatic configurations on VGS.

[Official Documentation](https://www.verygoodsecurity.com/docs/vgs-cli/getting-started)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Run](#run)
- [Running in Docker](#running-in-docker)
- [Commands](#commands)
- [Automation with VGS CLI](#automation-with-vgs-cli)
- [Sphinx Documentation](#sphinx-documentation)
- [Plugins Development](#plugins-development)

## Requirements
[Python 3](https://www.python.org/downloads/) or [Docker](https://docs.docker.com/get-docker/).

## Installation

### PyPI
Install the latest version from [PyPI](https://pypi.org/project/vgs-cli/):
```
pip install vgs-cli
```

## Run

Verify your installation by running:
```
vgs --version
```

## Running in Docker

Check our [official documentation](https://www.verygoodsecurity.com/docs/vgs-cli/docker).

## Commands

- [`help`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#exploring-the-cli)
- [`login`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#login)
- [`logout`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#logout)
- [`routes get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`routes apply`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#apply)
- [`logs access`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#access)

## Automation with VGS CLI

If you want to use the VGS CLI for automation you might be interested in creating a [service account](https://www.verygoodsecurity.com/docs/vgs-cli/service-account).

## Sphinx Documentation

In order to generate [Sphinx](https://www.sphinx-doc.org/en/master/index.html) documentation:
```
pip install -r dev-requirements.txt
cd docs
make html
```
Check the generated docs:
```
open build/html/index.html
```

## Plugins Development

See [Click - Developing Plugins](https://github.com/click-contrib/click-plugins#developing-plugins).

In order to develop a plugin you need to register your commands to an entrypoint in `setup.py`.

Supported entrypoints:

- `vgs.plugins` - for extending `vgs` with sub-commands
- `vgs.get.plugins` - for extending `vgs get` with sub-commands
- `vgs.apply.plugins` - for extending `vgs apply` with sub-commands
- `vgs.logs.plugins` - for extending `vgs logs` with sub-commands

Example:
```python
entry_points='''
    [vgs.plugins]
    activate=vgscliplugin.myplugin:new_command
    
    [vgs.get.plugins]
    preferences=vgscliplugin.myplugin:new_get_command
'''
```

### Plugin catalog
- [vgs-cli-admin-plugin](https://github.com/verygoodsecurity/vgs-cli-admin-plugin)
- [vgs-cli-marketplace-plugin](https://github.com/verygoodsecurity/vgs-cli-marketplace-plugin)
- [vgs-cli-marketplace-dev-plugin](https://github.com/verygoodsecurity/vgs-cli-marketplace-dev-plugin)
- [vgs-cli-compute-plugin](https://github.com/verygoodsecurity/vgs-cli-compute-plugin)
- [vgs-cli-athena-plugin](https://github.com/verygoodsecurity/vgs-cli-athena-plugin)
