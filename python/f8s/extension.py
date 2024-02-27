from typing import Optional  # noqa F401
import flask  # noqa F401

import yaml

from f8s.api import API
# ------------------------------------------------------------------------------


# inheriting from Singleton breaks init and init_app tests
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

    def init_app(self, app):
        # type: (flask.Flask) -> None
        '''
        Add endpoints and error handlers to given app.

        Args:
            app (Flask): Flask app.
        '''
        app.extensions['f8s'] = self
        app.register_blueprint(self.api)
        if not app.config['TESTING']:
            self.config = self.get_config(app)
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
        app.config.from_prefixed_env('F8S')
        secrets = app.config
        config_path = secrets.get('F8S_CONFIG_PATH', None)

        # create config
        config = {}
        if config_path is not None:
            with open(config_path) as f:
                config = yaml.safe_load(f)

        # update config with secrets
        config.update(secrets)
        return config

    def validate(self, config):
        # type: (dict) -> None
        '''
        Raises an error if given config is invalid.

        Args:
            config (dict): Extension config.
        '''
        pass
