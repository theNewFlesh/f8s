from pathlib import Path
from tempfile import TemporaryDirectory
import os
import time

import flask
import pytest
import yaml

import f8s
# ------------------------------------------------------------------------------


DELAY = 1


@pytest.fixture()
def config():
    return {}


@pytest.fixture()
def env(config):
    os.environ['F8S_SECRET_1'] = 'secret-1'
    os.environ['F8S_SECRET_2'] = 'secret-2'


@pytest.fixture()
def app():
    yield f8s.app.get_app(extensions=[], testing=True)


@pytest.fixture()
def client(app):
    yield app.server.test_client()


@pytest.fixture()
def flask_app():
    context = flask.Flask(__name__).app_context()
    context.push()
    app = context.app
    app.config['TESTING'] = True
    yield app
    context.pop()


@pytest.fixture()
def flask_client(flask_app):
    yield flask_app.test_client()


@pytest.fixture()
def extension(flask_app):
    flask_app.config['TESTING'] = False
    f8s.extension.swagger.init_app(flask_app)
    f8s.extension.f8s.init_app(flask_app)
    yield f8s.extension.f8s


@pytest.fixture()
def temp_dir():
    temp = TemporaryDirectory()
    yield temp.name
    temp.cleanup()


@pytest.fixture()
def config_yaml_file(temp_dir, config):
    filepath = Path(temp_dir, 'config.yaml').as_posix()
    with open(filepath, 'w') as f:
        yaml.safe_dump(config, f)

    os.environ['F8S_CONFIG_PATH'] = filepath
    return filepath


@pytest.fixture()
def api_setup(env, extension):
    return dict(env=env, extension=extension)


@pytest.fixture()
def api_demo(flask_client):
    response = flask_client.post('/api/demo')
    time.sleep(DELAY)
    yield response


@pytest.fixture()
def app_setup(env, app):
    yield dict(env=env, app=app)
