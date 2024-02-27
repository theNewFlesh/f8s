from typing import Callable, Optional

import flasgger
import flask
import flask_healthz
# ------------------------------------------------------------------------------


'''
A Flask REST application for Kuberenetes.
'''


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

    flasgger.Swagger().init_app(app)
    flask_healthz.Healthz().init_app(app)
    for ext in extensions:
        ext.init_app(app)

    return app
