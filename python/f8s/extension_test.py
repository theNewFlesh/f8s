import pytest

from f8s.extension import API, F8s
# ------------------------------------------------------------------------------


def test_init(env, flask_app):
    result = F8s(app=None)
    assert hasattr(result, 'config') is False

    flask_app.config['TESTING'] = False
    result = F8s(app=flask_app)
    assert hasattr(result, 'config')


def test_name():
    result = F8s(app=None).name
    assert result == 'f8s'

    class Foo(F8s):
        pass

    result = Foo().name
    assert result == 'foo'


def test_init_app(env, flask_app):
    flask_app.config['TESTING'] = False
    ext = F8s()
    ext.init_app(flask_app)

    assert flask_app.extensions['f8s'] is ext
    assert flask_app.blueprints['f8s'] is ext.api
    assert hasattr(ext, 'config')
    assert isinstance(ext.config, dict)


def test_init_app_config_path(env, flask_app, config, config_path):
    flask_app.config['TESTING'] = False
    ext = F8s()
    ext.init_app(flask_app)

    for key, val in config.items():
        assert ext.config[key] == val


def test_init_app_testing(env, flask_app, config_path):
    flask_app.config['TESTING'] = True
    ext = F8s()
    ext.init_app(flask_app)

    assert flask_app.extensions['f8s'] is ext
    assert flask_app.blueprints['f8s'] is API
    assert hasattr(ext, 'config') is False


def test_validate(foo_env, flask_app, config, config_path):
    flask_app.config['TESTING'] = False

    class Foo(F8s):
        def validate(self, config):
            assert config['foo'] != 'bar'

    ext = Foo()
    with pytest.raises(AssertionError):
        ext.init_app(flask_app)


def test_get_config(env, flask_app, config, config_path):
    flask_app.config['TESTING'] = False

    result = F8s(app=None).get_config(flask_app)
    for key, val in config.items():
        assert result[key] == val

    assert result['SECRET_1'] == 'secret-1'
    assert result['SECRET_2'] == 'secret-2'
