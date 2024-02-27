import json

import flask
import flasgger as swg

from f8s.extension import F8s
import f8s.tools as f8st


# API---------------------------------------------------------------------------
API = flask.Blueprint('test', __name__, url_prefix='')


@API.route('/api/v1/get', methods=['GET'])
@swg.swag_from(dict(
    parameters=[],
    responses={
        200: dict(
            description='test endpoint.',
            content='application/json',
        ),
        500: dict(
            description='Internal server error.',
        )
    }
))
def get():
    # type: () -> flask.Response
    '''
    Get test response.

    Returns:
        Response: Flask Response instance.
    '''
    return flask.Response(
        response=json.dumps(dict(message='Success')),
        mimetype='application/json'
    )


@API.route('/api/v1/post', methods=['POST'])
@swg.swag_from(dict(
    parameters=[
        dict(
            name='params',
            type='dict',
            description='Test params.',
            required=True,
        )
    ],
    responses={
        200: dict(description='JSON data', content='application/json'),
        500: dict(description='Internal server error.')
    }
))
def post():
    # type: () -> flask.Response
    '''
    Post test data.

    Returns:
        Response: Flask Response instance.
    '''
    data = json.loads(flask.request.json)  # type: ignore
    return flask.Response(
        response=json.dumps(data),
        mimetype='application/json'
    )


@API.route('/api/v1/config', methods=['GET'])
@swg.swag_from(dict(
    parameters=[],
    responses={
        200: dict(description='Config data', content='application/json'),
        500: dict(description='Internal server error.')
    }
))
def config():
    # type: () -> flask.Response
    '''
    Get config data.

    Returns:
        Response: Flask Response instance.
    '''
    data = flask.current_app.config['demo']
    return flask.Response(
        response=json.dumps(data),
        mimetype='application/json'
    )


# EXTENSION---------------------------------------------------------------------
class Demo(F8s):
    api = API

    def validate(self, config):
        if 'foo' in config.keys():
            assert config['foo'] == 'bar'


def live_probe():
    # type: () -> dict
    '''
    Liveness probe for kubernetes.
    '''
    return dict(status='live')


def ready_probe():
    # type: () -> dict
    '''
    Readiness probe for kubernetes.
    '''
    return dict(status='ready')


# APP---------------------------------------------------------------------------
def get_app():
    return f8st.get_app([Demo()], live_probe, ready_probe)


app = get_app()
