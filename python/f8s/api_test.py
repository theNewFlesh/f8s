import json
import time

import pytest
# ------------------------------------------------------------------------------


RERUNS = 3
DELAY = 0.1


def try_post_json(
    client, url, json=None, status=None, attempts=10, delay=DELAY
):
    error = 'try_post_json failed.'
    response = None
    for _ in range(attempts):
        try:
            response = client.post(url, json=json)
        except Exception as error:  # noqa: F841
            error = error.args[0]
        time.sleep(delay)

        if status is not None and response.status_code != status:
            error = response.text  # type: ignore
            continue
        return response.json

    raise RuntimeError(error)


@pytest.mark.flaky(reruns=RERUNS)
def test_endpoint(api_setup, flask_client, make_files, api_update):
    extension = api_setup['extension']

    # call test
    result = try_post_json(
        flask_client, '/api/test', json={}, status=200
    )['response']
    expected = extension.database.test() \
        .replace({np.nan: None}) \
        .to_dict(orient='records')
    assert result == expected

    # test general exceptions
    extension.database = 'foo'
    result = try_post_json(flask_client, '/api/test', json={})['error']
    assert result == 'AttributeError'


# ERROR-HANDLERS----------------------------------------------------------------
@pytest.mark.flaky(reruns=RERUNS)
def test_key_error_handler(api_setup, flask_client, make_files):
    result = flask_client.post(
        '/api/workflow',
        json=json.dumps(dict()),
    ).json
    assert result['error'] == 'KeyError'


@pytest.mark.flaky(reruns=RERUNS)
def test_type_error_handler(api_setup, flask_client, make_files):
    result = flask_client.post('/api/workflow', json=json.dumps([])).json
    assert result['error'] == 'TypeError'


@pytest.mark.flaky(reruns=RERUNS)
def test_json_decode_error_handler(api_setup, flask_client, make_files):
    result = flask_client.post('/api/workflow', json='bad json').json
    assert result['error'] == 'JSONDecodeError'
