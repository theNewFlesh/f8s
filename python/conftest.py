from pathlib import Path
from tempfile import TemporaryDirectory
import os

import flask
import pytest
import yaml

import f8s.test_app as f8sta
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


@pytest.fixture()
def env(config_path):
    os.environ['F8S_CONFIG_PATH'] = config_path
    os.environ['F8S_SECRET_1'] = 'secret-1'
    os.environ['F8S_SECRET_2'] = 'secret-2'
    yield
    del os.environ['F8S_CONFIG_PATH']
    del os.environ['F8S_SECRET_1']
    del os.environ['F8S_SECRET_2']


@pytest.fixture()
def foo_env(config_path):
    os.environ['FOO_CONFIG_PATH'] = config_path
    os.environ['FOO_SECRET_1'] = 'secret-1'
    os.environ['FOO_SECRET_2'] = 'secret-2'
    yield
    del os.environ['FOO_CONFIG_PATH']
    del os.environ['FOO_SECRET_1']
    del os.environ['FOO_SECRET_2']


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
    app = f8sta.get_app()
    context = app.app_context()
    context.push()
    app = context.app
    app.config['TESTING'] = True
    yield app
    context.pop()


@pytest.fixture()
def client(test_app):
    yield test_app.test_client()
