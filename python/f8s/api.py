from typing import Any  # noqa F401

from json import JSONDecodeError

import flask

import f8s.tools
# ------------------------------------------------------------------------------


'''
Generic F8s API.
'''


API = flask.Blueprint('f8s', __name__, url_prefix='')


@API.route('/apidocs')
def apidocs():
    # type: () -> Any
    '''
    Route to F8s API documentation.

    Returns:
        html: Flassger generated API page.
    '''
    return flask.redirect(flask.url_for('flasgger.apidocs'))


@API.errorhandler(KeyError)
def handle_key_error(error):
    # type: (KeyError) -> flask.Response
    '''
    Handles key errors.

    Args:
        error (KeyError): Key error.

    Returns:
        Response: KeyError response.
    '''
    return f8s.tools.error_to_response(error)


@API.errorhandler(TypeError)
def handle_type_error(error):
    # type: (TypeError) -> flask.Response
    '''
    Handles type errors.

    Args:
        error (TypeError): Type error.

    Returns:
        Response: TypeError response.
    '''
    return f8s.tools.error_to_response(error)


@API.errorhandler(JSONDecodeError)
def handle_json_decode_error(error):
    # type: (JSONDecodeError) -> flask.Response
    '''
    Handles JSON decoding errors.

    Args:
        error (JSONDecodeError): JSONDecodeError error.

    Returns:
        Response: JSONDecodeError response.
    '''
    return f8s.tools.error_to_response(error)
# ------------------------------------------------------------------------------


API.register_error_handler(500, handle_key_error)
API.register_error_handler(500, handle_type_error)
API.register_error_handler(500, handle_json_decode_error)
