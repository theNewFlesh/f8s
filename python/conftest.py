from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import time

import flask
import pytest
import yaml

import f8s.app as application
import f8s.extension as ext
# ------------------------------------------------------------------------------


DELAY = 1


@pytest.fixture()
def env(config):
    yaml_keys = [
        'specification_files',
        'exporters',
        'webhooks',
    ]
    for key, val in config.items():
        if key in yaml_keys:
            os.environ[f'HIDEBOUND_{key.upper()}'] = yaml.safe_dump(val)
        elif key == 'dask':
            for k, v in val.items():
                os.environ[f'HIDEBOUND_DASK_{k.upper()}'] = str(v)
        else:
            os.environ[f'HIDEBOUND_{key.upper()}'] = str(val)

    keys = filter(lambda x: x.startswith('HIDEBOUND_'), os.environ.keys())
    env = {k: os.environ[k] for k in keys}
    yield env

    keys = filter(lambda x: x.startswith('HIDEBOUND_'), os.environ.keys())
    for key in keys:
        os.environ.pop(key)


@pytest.fixture()
def app():
    yield application.APP


@pytest.fixture()
def app_client(app):
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
    ext.swagger.init_app(flask_app)
    ext.hidebound.init_app(flask_app)
    ext.hidebound.database._testing = True
    yield ext.hidebound


@pytest.fixture()
def temp_dir():
    temp = TemporaryDirectory()
    yield temp.name
    temp.cleanup()


@pytest.fixture()
def config_yaml_file(temp_dir, config):
    filepath = Path(temp_dir, 'hidebound_config.yaml').as_posix()
    with open(filepath, 'w') as f:
        yaml.safe_dump(config, f)

    os.environ['HIDEBOUND_CONFIG_FILEPATH'] = filepath
    return filepath


@pytest.fixture()
def config_json_file(temp_dir, config):
    filepath = Path(temp_dir, 'hidebound_config.json').as_posix()
    with open(filepath, 'w') as f:
        json.dump(config, f)

    os.environ['HIDEBOUND_CONFIG_FILEPATH'] = filepath
    return filepath


@pytest.fixture()
def api_setup(env, extension):
    return dict(
        env=env,
        extension=extension,
    )


@pytest.fixture()
def api_update(flask_client):
    response = flask_client.post('/api/update')
    time.sleep(DELAY)
    yield response


@pytest.fixture()
def app_setup(env, app):
    yield dict(env=env, app=app)
