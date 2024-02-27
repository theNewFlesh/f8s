from pathlib import Path
from tempfile import TemporaryDirectory
import os
import time

import flask
import pytest
import yaml

import f8s
import f8s.test_app as f8sta
# ------------------------------------------------------------------------------


DELAY = 1


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


# @pytest.fixture()
# def app():
#     yield f8s.app.get_app(extensions=[], testing=True)


# @pytest.fixture()
# def client(app):
#     yield app.server.test_client()



# @pytest.fixture()
# def extension(flask_app):
#     flask_app.config['TESTING'] = False
#     f8s.extension.swagger.init_app(flask_app)
#     f8s.extension.f8s.init_app(flask_app)
#     yield f8s.extension.f8s


# @pytest.fixture()
# def api_setup(env, extension):
#     return dict(env=env, extension=extension)


# @pytest.fixture()
# def api_demo(flask_client):
#     response = flask_client.post('/api/demo')
#     time.sleep(DELAY)
#     yield response


# @pytest.fixture()
# def app_setup(env, app):
#     yield dict(env=env, app=app)
