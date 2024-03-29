from pathlib import Path
from tempfile import TemporaryDirectory
import os

import flask
import pytest
import yaml

import f8s.test_app as f8a
# ------------------------------------------------------------------------------


@pytest.fixture()
def config():
    return dict(foo='bar')


@pytest.fixture()
def config_path(config):
    temp = TemporaryDirectory()
    filepath = Path(temp.name, 'config.yaml').as_posix()
    with open(filepath, 'w') as f:
        yaml.safe_dump(config, f)
    yield filepath
    temp.cleanup()


def env_setup(config_path, prefix='F8S'):
    os.environ[f'{prefix}_CONFIG_PATH'] = config_path
    os.environ[f'{prefix}_SECRET_1'] = 'secret-1'
    os.environ[f'{prefix}_SECRET_2'] = 'secret-2'
    keys = filter(lambda x: x.startswith(prefix), os.environ.keys())
    return {k: os.environ[k] for k in keys}


def env_teardown(prefix='F8S'):
    del os.environ[f'{prefix}_CONFIG_PATH']
    del os.environ[f'{prefix}_SECRET_1']
    del os.environ[f'{prefix}_SECRET_2']


@pytest.fixture()
def env(config_path):
    yield env_setup(config_path)
    env_teardown()


@pytest.fixture()
def demo_env(config_path):
    yield env_setup(config_path, 'DEMO')
    env_teardown('DEMO')


@pytest.fixture()
def flask_app():
    context = flask.Flask(__name__).app_context()
    context.push()
    app = context.app
    app.config['TESTING'] = True
    yield app
    context.pop()


@pytest.fixture()
def test_app():
    app = f8a.get_app()
    context = app.app_context()
    context.push()
    app = context.app
    app.config['TESTING'] = True
    yield app
    context.pop()


@pytest.fixture()
def client(test_app):
    yield test_app.test_client()
