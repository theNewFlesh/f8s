import os

import flask
import pytest

import f8s
# ------------------------------------------------------------------------------


def test_liveness(app_setup, client):
    result = client.get('/healthz/live').status_code
    assert result == 200


def test_readiness(app_setup, client):
    result = client.get('/healthz/ready').status_code
    assert result == 200


@pytest.mark.skipif('SKIP_SLOW_TESTS' in os.environ, reason='slow test')
def test_get_app(app_setup):
    result = f8s.app.get_app(testing=True)
    assert isinstance(result, flask.Flask)
