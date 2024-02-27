from typing import Any, Callable, Optional  # noqa F401

from pprint import pformat
import json
import traceback

import flask
import flasgger
import flask_healthz
# ------------------------------------------------------------------------------


'''
K8s ready Flask REST application tools.
'''


swagger = flasgger.Swagger()
healthz = flask_healthz.Healthz()


def error_to_response(error):
    # type: (Exception) -> flask.Response
    '''
    Convenience function for formatting a given exception as a Flask Response.

    Args:
        error (Exception): Error to be formatted.

    Returns:
        flask.Response: Flask response.
    '''
    args = []  # type: Any
    for arg in error.args:
        if hasattr(arg, 'items'):
            for key, val in arg.items():
                args.append(pformat({key: pformat(val)}))
        else:
            args.append(str(arg))
    args = ['    ' + x for x in args]
    args = '\n'.join(args)
    klass = error.__class__.__name__
    msg = f'{klass}(\n{args}\n)'
    return flask.Response(
        response=json.dumps(dict(
            error=error.__class__.__name__,
            args=list(map(str, error.args)),
            message=msg,
            code=500,
            traceback=traceback.format_exc(),
        )),
        mimetype='application/json',
        status=500,
    )


def get_app(extensions, live_probe=None, ready_probe=None, testing=False):
    # type: (list, Optional[Callable], Optional[Callable], bool) -> flask.Flask
    '''
    Creates a F8S app.

    Returns:
        flask.Flask: Flask app.
    '''
    noop = lambda: None
    if live_probe is None:
        live_probe = noop

    if ready_probe is None:
        ready_probe = noop

    app = flask.Flask('F8s')
    app.config['TESTING'] = testing
    app.config['HEALTHZ'] = dict(live=live_probe, ready=ready_probe)

    swagger.init_app(app)
    healthz.init_app(app)
    for ext in extensions:
        ext.init_app(app)

    return app
