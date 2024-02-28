<p>
    <a href="https://www.linkedin.com/in/alexandergbraun" rel="nofollow noreferrer">
        <img src="https://www.gomezaparicio.com/wp-content/uploads/2012/03/linkedin-logo-1-150x150.png"
             alt="linkedin" width="30px" height="30px"
        >
    </a>
    <a href="https://github.com/theNewFlesh" rel="nofollow noreferrer">
        <img src="https://tadeuzagallo.com/GithubPulse/assets/img/app-icon-github.png"
             alt="github" width="30px" height="30px"
        >
    </a>
    <a href="https://pypi.org/user/theNewFlesh" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-256/python-2-226051.png"
             alt="pypi" width="30px" height="30px"
        >
    </a>
    <a href="http://vimeo.com/user3965452" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-512/movie-52-151107.png?f=avif&w=512"
             alt="vimeo" width="30px" height="30px"
        >
    </a>
    <a href="http://www.alexgbraun.com" rel="nofollow noreferrer">
        <img src="https://i.ibb.co/fvyMkpM/logo.png"
             alt="alexgbraun" width="30px" height="30px"
        >
    </a>
</p>

<!-- <img id="logo" src="resources/logo.png" style="max-width: 717px"> -->

[![](https://img.shields.io/badge/License-MIT-F77E70?style=for-the-badge)](https://github.com/theNewFlesh/f8s/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/f8s?style=for-the-badge&label=Python&color=A0D17B&logo=python&logoColor=A0D17B)](https://github.com/theNewFlesh/f8s/blob/master/docker/config/pyproject.toml)
[![](https://img.shields.io/pypi/v/f8s?style=for-the-badge&label=PyPI&color=5F95DE&logo=pypi&logoColor=5F95DE)](https://pypi.org/project/f8s/)
[![](https://img.shields.io/pypi/dm/f8s?style=for-the-badge&label=Downloads&color=5F95DE)](https://pepy.tech/project/f8s)

# Introduction

Framework for building K8s-ready Flask applications.

See [documentation](https://theNewFlesh.github.io/f8s/) for details.

# Installation
### Python
`pip install f8s`

### Docker
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. `docker pull theNewFlesh/f8s:[version]`

### Docker For Developers
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. Ensure docker-desktop has at least 4 GB of memory allocated to it.
3. `git clone git@github.com:theNewFlesh/f8s.git`
4. `cd f8s`
5. `chmod +x bin/f8s`
6. `bin/f8s docker-start`

The service should take a few minutes to start up.

Run `bin/f8s --help` for more help on the command line tool.

### ZSH Setup

1. `bin/f8s` must be run from this repository's top level directory.
2. Therefore, if using zsh, it is recommended that you paste the following line
    in your ~/.zshrc file:
    - `alias f8s="cd [parent dir]/f8s; bin/f8s"`
    - Replace `[parent dir]` with the parent directory of this repository
3. Running the `zsh-complete` command will enable tab completions of the cli
   commands, in the next shell session.

   For example:
   - `f8s [tab]` will show you all the cli options, which you can press
     tab to cycle through
   - `f8s docker-[tab]` will show you only the cli options that begin with
     "docker-"

---

# App Development

F8s apps are designed to create a parity between ConfigMap/Secret values and
internal Flask configuration per extension. Relevant yaml files and environment
variables mapped into the container are aggregated by each extension and
accesible via `flask.current_app.config[extension_name]` in python.

The helm chart can be used as is for deploying your app or it can copied to a
separate git repo and modified to your requirements.

### Example Helm values.yaml

```yaml
extensions:
  rest: |                 # creates `REST_CONFIG_PATH=~/f8s/rest-config.yaml` env var
    allowed-actions:      # `~/f8s/rest-config.yaml` content
      - get
      - post
  db: |                   # creates `DB_CONFIG_PATH=~/f8s/db-config.yaml` env var
    user: admin           # `~/f8s/db-config.yaml` content
    tables:
      - users
      - groups

secret: |                 # create additional env vars
  REST_TOKEN: token       # vars need to begin with extension such as REST_ or DB_
  DB_PASSWORD: pwd
  DB_TOKEN: token

deployment:
  config_directory: /home/ubuntu/f8s  # the directory for all the extension config files
  repository: thenewflesh/f8s
  image_tag: prod-latest
```

### Example Python app.py

```python
import json

import database  # example database
import flask
import flasgger as swg

from f8s.extension import F8s
import f8s.tools as f8s_tools


# DB----------------------------------------------------------------------------
# blueprint
DB_API = flask.Blueprint('db', __name__, url_prefix='')


# api
@DB_API.route('/api/v1/query', methods=['POST'])  # flask route decorator
@swg.swag_from(dict(                              # swagger apidocs decorator
    parameters=[
        dict(
            name='query',
            type='dict',
            description='DB query',
            required=True,
        )
    ],
    responses={
        200: dict(description='JSON data', content='application/json'),
        500: dict(description='Internal server error.')
    }
))
def query():
    data = json.loads(flask.request.json)
    result = database.query(data)
    return flask.Response(
        response=json.dumps(result),
        mimetype='application/json'
    )

# F8s extension
class DB(F8s):    # class name determines env var prefixes
    api = DB_API  # api class member needs to be assigned to a blueprint


# REST--------------------------------------------------------------------------
# blueprint
REST_API = flask.Blueprint('rest', __name__, url_prefix='')


# api
@REST_API.route('/api/v1/config', methods=['GET'])  # flask route decorator
@swg.swag_from(dict(                                # swagger apidocs decorator
    parameters=[],
    responses={
        200: dict(description='Config data', content='application/json'),
        500: dict(description='Internal server error.')
    }
))
def config():
    # cfg is configuration for rest extension
    # it is the contents of /home/ubuntu/f8s/rest-config.yaml plus the env vars
    # that start with REST_, such as REST_CONFIG_PATH and REST_TOKEN
    cfg = flask.current_app.config['rest']  # key name is lowercase class name
    return flask.Response(
        response=json.dumps(cfg),
        mimetype='application/json'
    )


# F8s extension
class REST(F8s):    # class name determines env var prefixes
    api = REST_API  # api class member needs to be assigned to a blueprint

    def validate(self, config):  # additional validation of config dictionary
        assert isinstance(config['allowed-actions'], list)


# HEALTHZ-PROBES----------------------------------------------------------------
def live_probe():
    return database.connected()


def ready_probe():
    return True


# APP---------------------------------------------------------------------------
def get_app():
    # returns a Flask with both DB and REST blueprints and both health probes
    return f8s_tools.get_app([DB(), REST()], live_probe, ready_probe)


app = get_app()  # app variable needs to exist for gunicorn to call
```

### Absolute minimum python boilerplate

```python
import flask

from f8s.extension import F8s
import f8s.tools as f8s_tools

API = flask.Blueprint('hello', __name__, url_prefix='')

@API.route('/api/v1/hello')
def hello():
    return 'hello'

class Hello(F8s):
    api = API

app = f8s_tools.get_app([Hello()])
```

### Serve F8s App

```shell
f8s serve /path/to/app.py
```

---

# Quickstart Guide
This repository contains a suite commands for the whole development process.
This includes everything from testing, to documentation generation and
publishing pip packages.

These commands can be accessed through:

  - The VSCode task runner
  - The VSCode task runner side bar
  - A terminal running on the host OS
  - A terminal within this repositories docker container

Running the `zsh-complete` command will enable tab completions of the CLI.
See the zsh setup section for more information.

### Command Groups

Development commands are grouped by one of 10 prefixes:

| Command    | Description                                                                        |
| ---------- | ---------------------------------------------------------------------------------- |
| build      | Commands for building packages for testing and pip publishing                      |
| docker     | Common docker commands such as build, start and stop                               |
| docs       | Commands for generating documentation and code metrics                             |
| library    | Commands for managing python package dependencies                                  |
| session    | Commands for starting interactive sessions such as jupyter lab and python          |
| state      | Command to display the current state of the repo and container                     |
| test       | Commands for running tests, linter and type annotations                            |
| version    | Commands for bumping project versions                                              |
| quickstart | Display this quickstart guide                                                      |
| zsh        | Commands for running a zsh session in the container and generating zsh completions |

### Common Commands

Here are some frequently used commands to get you started:

| Command           | Description                                               |
| ----------------- | --------------------------------------------------------- |
| docker-restart    | Restart container                                         |
| docker-start      | Start container                                           |
| docker-stop       | Stop container                                            |
| docs-full         | Generate documentation, coverage report, diagram and code |
| library-add       | Add a given package to a given dependency group           |
| library-graph-dev | Graph dependencies in dev environment                     |
| library-remove    | Remove a given package from a given dependency group      |
| library-search    | Search for pip packages                                   |
| library-update    | Update dev dependencies                                   |
| session-lab       | Run jupyter lab server                                    |
| state             | State of                                                  |
| test-dev          | Run all tests                                             |
| test-lint         | Run linting and type checking                             |
| zsh               | Run ZSH session inside container                          |
| zsh-complete      | Generate ZSH completion script                            |

---

# Development CLI
bin/f8s is a command line interface (defined in cli.py) that
works with any version of python 2.7 and above, as it has no dependencies.
Commands generally do not expect any arguments or flags.

Its usage pattern is: `bin/f8s COMMAND [-a --args]=ARGS [-h --help] [--dryrun]`

### Commands
The following is a complete list of all available development commands:

| Command                 | Description                                                         |
| ----------------------- | ------------------------------------------------------------------- |
| build-package           | Build production version of repo for publishing                     |
| build-prod              | Publish pip package of repo to PyPi                                 |
| build-publish           | Run production tests first then publish pip package of repo to PyPi |
| build-test              | Build test version of repo for prod testing                         |
| docker-build            | Build Docker image                                                  |
| docker-build-from-cache | Build Docker image from cached image                                |
| docker-build-prod       | Build production image                                              |
| docker-container        | Display the Docker container id                                     |
| docker-destroy          | Shutdown container and destroy its image                            |
| docker-destroy-prod     | Shutdown production container and destroy its image                 |
| docker-image            | Display the Docker image id                                         |
| docker-prod             | Start production container                                          |
| docker-pull-dev         | Pull development image from Docker registry                         |
| docker-pull-prod        | Pull production image from Docker registry                          |
| docker-push-dev         | Push development image to Docker registry                           |
| docker-push-dev-latest  | Push development image to Docker registry with dev-latest tag       |
| docker-push-prod        | Push production image to Docker registry                            |
| docker-push-prod-latest | Push production image to Docker registry with prod-latest tag       |
| docker-remove           | Remove Docker image                                                 |
| docker-restart          | Restart Docker container                                            |
| docker-start            | Start Docker container                                              |
| docker-stop             | Stop Docker container                                               |
| docs                    | Generate sphinx documentation                                       |
| docs-architecture       | Generate architecture.svg diagram from all import statements        |
| docs-full               | Generate documentation, coverage report, diagram and code           |
| docs-metrics            | Generate code metrics report, plots and tables                      |
| library-add             | Add a given package to a given dependency group                     |
| library-graph-dev       | Graph dependencies in dev environment                               |
| library-graph-prod      | Graph dependencies in prod environment                              |
| library-install-dev     | Install all dependencies into dev environment                       |
| library-install-prod    | Install all dependencies into prod environment                      |
| library-list-dev        | List packages in dev environment                                    |
| library-list-prod       | List packages in prod environment                                   |
| library-lock-dev        | Resolve dev.lock file                                               |
| library-lock-prod       | Resolve prod.lock file                                              |
| library-remove          | Remove a given package from a given dependency group                |
| library-search          | Search for pip packages                                             |
| library-sync-dev        | Sync dev environment with packages listed in dev.lock               |
| library-sync-prod       | Sync prod environment with packages listed in prod.lock             |
| library-update          | Update dev dependencies                                             |
| library-update-pdm      | Update PDM                                                          |
| quickstart              | Display quickstart guide                                            |
| session-lab             | Run jupyter lab server                                              |
| session-python          | Run python session with dev dependencies                            |
| session-server          | Runn application server inside Docker container                     |
| state                   | State of repository and Docker container                            |
| test-coverage           | Generate test coverage report                                       |
| test-dev                | Run all tests                                                       |
| test-fast               | Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator  |
| test-lint               | Run linting and type checking                                       |
| test-prod               | Run tests across all support python versions                        |
| version                 | Full resolution of repo: dependencies, linting, tests, docs, etc    |
| version-bump-major      | Bump pyproject major version                                        |
| version-bump-minor      | Bump pyproject minor version                                        |
| version-bump-patch      | Bump pyproject patch version                                        |
| version-commit          | Tag with version and commit changes to master                       |
| zsh                     | Run ZSH session inside Docker container                             |
| zsh-complete            | Generate oh-my-zsh completions                                      |
| zsh-root                | Run ZSH session as root inside Docker container                     |

### Flags

| Short | Long      | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| -a    | --args    | Additional arguments, this can generally be ignored  |
| -h    | --help    | Prints command help message to stdout                |
|       | --dryrun  | Prints command that would otherwise be run to stdout |

---

# Production CLI

f8s comes with a command line interface defined in command.py.

Its usage pattern is: `f8s COMMAND [ARGS] [FLAGS] [-h --help]`

## Commands

---

### bash-completion
Prints BASH completion code to be written to a _f8s completion file

Usage: `f8s bash-completion`

---

### serve
Serves given F8s application via gunicorn

Usage: `f8s serve app.py app`

---

### zsh-completion
Prints ZSH completion code to be written to a _f8s completion file

Usage: `f8s zsh-completion`

