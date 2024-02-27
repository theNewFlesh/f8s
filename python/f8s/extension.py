from typing import Any, Optional  # noqa F401

import os
import re

import flask
import yaml
# ------------------------------------------------------------------------------


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
# ------------------------------------------------------------------------------


class F8s:
    api = API

    def __init__(self, app=None):
        # type: (Optional[flask.Flask]) -> None
        '''
        Initialize flask extension.

        Args:
            app (flask.Flask, optional): Flask app.
        '''
        if app is not None:
            self.init_app(app)

    @property
    def name(self):
        # type: () -> str
        '''
        Returns:
            str: Name of class.
        '''
        return self.__class__.__name__.lower()

    def init_app(self, app):
        # type: (flask.Flask) -> None
        '''
        Add endpoints and error handlers to given app.

        Args:
            app (Flask): Flask app.
        '''
        app.extensions[self.name] = self
        app.register_blueprint(self.api)
        if not app.config['TESTING']:
            self.config = self.get_config(app)
            app.config[self.name] = self.config
            self.validate(self.config)

    def get_config(self, app):
        # type: (flask.Flask) -> dict
        '''
        Get config from envirnment variables or config file.

        Args:
            app (flask.Flask): Flask app.

        Returns:
            dict: Database config.
        '''
        # get config variables from environment
        prefix = self.name.upper() + '_'
        env = {}
        for key, val in os.environ.items():
            if key.startswith(prefix):
                k = re.sub(f'^{prefix}', '', key).lower()
                env[k] = val

        # create config
        config_path = env.get('config_path', None)
        config = {}
        if config_path is not None:
            with open(config_path) as f:
                config = yaml.safe_load(f)

        # update config with env vars
        config.update(env)
        return config

    def validate(self, config):
        # type: (dict) -> None
        '''
        Raises an error if given config is invalid.

        Args:
            config (dict): Extension config.
        '''
        pass
