import json

import flask
import flasgger as swg

import f8s.app as f8s_app
from f8s.extension import F8s
# ------------------------------------------------------------------------------


API = flask.Blueprint('demo', __name__, url_prefix='')


@API.route('/api/v1/demo', methods=['GET'])
@swg.swag_from(dict(
    parameters=[],
    responses={
        200: dict(
            description='Demo endpoint.',
            content='application/json',
        ),
        500: dict(
            description='Internal server error.',
        )
    }
))
def demo():
    # type: () -> flask.Response
    '''
    Create data.

    Returns:
        Response: Flask Response instance.
    '''
    return flask.Response(
        response=json.dumps(dict(message='Demo endpoint called.')),
        mimetype='application/json'
    )


class Demo(F8s):
    api = API

    # def validate(self, config):
    #     assert config['foo'] == 'bar'


def live_probe():
    # type: () -> None
    '''
    Liveness probe for kubernetes.
    '''
    pass


def ready_probe():
    # type: () -> None
    '''
    Readiness probe for kubernetes.
    '''
    pass


if __name__ == '__main__':
    extensions = [Demo()]
    app = f8s_app.get_app(extensions, live_probe, ready_probe)
    app.run(host='0.0.0.0', port=8080)
