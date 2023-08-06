# pylint: disable=missing-class-docstring, import-error, missing-function-docstring
from pytest import fail
from syncari.rest.client import SyncariException, SyncariRestClient
from syncari.logger import SyncariLogger

logger = SyncariLogger.get_logger('test_router')

def test_get():
    rest_client = SyncariRestClient('http://universities.hipolabs.com/', None)
    resp = rest_client.get('search?country=United+States')
    assert resp.status_code == 200
    university_names = [university['name'] for university in resp.json()]
    assert 'Stanford University' in university_names

def test_rest_request():
    rest_client = SyncariRestClient('http://universities.hipolabs.com/', None)
    resp = rest_client.get('search?country=United+States')
    assert resp.status_code == 200
    university_names = [university['name'] for university in resp.json()]
    assert 'Stanford University' in university_names

def test_get_error_response():
    rest_client = SyncariRestClient('http://universities.hipolabs.com/', None)
    # invalid path `searc`
    try:
        resp = rest_client.get('searc?country=United+States')
    except SyncariException as e:
        assert e.error_response.status_code == 404
        assert e.error_response.message == 'Failed to execute GET on url:http://universities.hipolabs.com/searc?country=United+States'
    except Exception as e:
        fail('Invalid exception thrown from SyncariRestClient')

def test_get_exception():
    # missing / in the host.
    rest_client = SyncariRestClient('http://universities.hipolabs.com', None)
    try:
        resp = rest_client.get('search?country=United+States')
    except SyncariException as e:
        assert e.error_response.status_code == 400
        assert e.error_response.message == 'Failed to execute GET on url:http://universities.hipolabs.comsearch?country=United+States'
    except Exception as e:
        fail('Invalid exception thrown from SyncariRestClient')

def test_post():
    rest_client = SyncariRestClient('https://api.provarity.com/', None)
    auth_data = {'user':'customer+syncari_admin@provarity.com', 'pass':'U3luY2FyaTF8Y3VzdG9tZXIrc3luY2FyaV9hZG1pbkBwcm92YXJpdHkuY29t'}
    resp = rest_client.post('user/login/provarity', json=auth_data)
    assert resp.status_code == 200
    resp_json = resp.json()
    resp_token_key = resp.json()['token']['key']
    assert resp_token_key is not None
