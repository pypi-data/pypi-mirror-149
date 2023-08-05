
# pylint: disable=missing-class-docstring, import-error, missing-function-docstring
import json
import pytest
from syncari.models.core import (AuthConfig, Connection, AuthType, 
    AuthField, AuthMetadata, UIMetadata, SynapseInfo, InitConnectionInfo)
from syncari.models.request import (DescribeRequest,
    Request, Response, SyncRequest, Watermark, WebhookRequest, RequestType)
from syncari.models.schema import Schema

from syncari.synapse.abstract_synapse import Synapse

class MockSynapse(Synapse):

    def __print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    @classmethod
    def __get_mock_response(cls, req_type):
        mock_values = {'name':req_type.name}
        return Response(body=json.dumps(mock_values))

    def connect(self):
        init_connection_response = InitConnectionInfo(connection=self.connection)
        return Response(body=init_connection_response.json())

    def synapse_info(self):
        return Response(body=SynapseInfo(
            name='test_synapse',category='crm',
            metadata=UIMetadata(displayName='Test Synapse'),
            supportedAuthTypes=[AuthMetadata(authType=AuthType.BASIC_TOKEN)],
            configuredFields=[AuthField(name='CRM ID')]).json())

    def describe(self):
        self.__print(self.describe.__name__, self.request)
        return self.__get_mock_response(RequestType.DESCRIBE)

    def read(self):
        self.__print(self.read.__name__, self.request)
        return self.__get_mock_response(RequestType.READ)

    def get(self):
        self.__print(self.get.__name__, self.request)
        return self.__get_mock_response(RequestType.GET)

    def create(self):
        self.__print(self.create.__name__, self.request)
        return self.__get_mock_response(RequestType.CREATE)

    def update(self):
        self.__print(self.update.__name__, self.request)
        return self.__get_mock_response(RequestType.UPDATE)

    def delete(self):
        self.__print(self.delete.__name__, self.request)
        return self.__get_mock_response(RequestType.DELETE)

    def extract_webhook_identifier(self):
        self.__print(self.extract_webhook_identifier.__name__, self.request)
        return self.__get_mock_response(RequestType.EXTRACT_WEBHOOK_IDENTIFIER)

    def process_webhook(self):
        self.__print(self.process_webhook.__name__, self.request)
        return self.__get_mock_response(RequestType.PROCESS_WEBHOOK)

class MockErrorSynapse(MockSynapse):
    def __print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    @classmethod
    def __get_mock_error_response(cls, req_type):
        mock_values = {'error':'error_str_' + req_type.name}
        return Response(body=json.dumps(mock_values))

    def init(self):
        return None

    def synapse_info(self):
        return None

    def describe(self):
        self.__print(self.describe.__name__, self.request)
        return self.__get_mock_error_response(RequestType.DESCRIBE)

    def read(self):
        self.__print(self.read.__name__, self.request)
        return self.__get_mock_error_response(RequestType.READ)

    def get(self):
        self.__print(self.get.__name__, self.request)
        return self.__get_mock_error_response(RequestType.GET)

    def create(self):
        self.__print(self.create.__name__, self.request)
        return self.__get_mock_error_response(RequestType.CREATE)
    
    def update(self):
        self.__print(self.create.__name__, self.request)
        return self.__get_mock_error_response(RequestType.UPDATE)

    def delete(self):
        self.__print(self.delete.__name__, self.request)
        return self.__get_mock_error_response(RequestType.DELETE)

    def extract_webhook_identifier(self):
        self.__print(self.extract_webhook_identifier.__name__, self.request)
        return self.__get_mock_error_response(RequestType.EXTRACT_WEBHOOK_IDENTIFIER)

    def process_webhook(self):
        self.__print(self.process_webhook.__name__, self.request)
        return self.__get_mock_error_response(RequestType.PROCESS_WEBHOOK)

class InvalidSynapse():
    def __init__(self) -> None:
        pass

def __get_describe_synapse_request():
    return Request(type=RequestType.DESCRIBE,
        connection=get_connection(),
        body=DescribeRequest(entities=['test'])).json()

def __get_read_synapse_request():
    return Request(type=RequestType.READ,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()

def __get_crud_synapse_request():
    return Request(type=RequestType.GET,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0)))

def __get_process_webook_request():
    return Request(type=RequestType.PROCESS_WEBHOOK,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()

def __assert_route(synapse_request):
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    print(resp)
    assert resp is not None
    expected = json.loads(resp.body)
    assert expected['name'].casefold() == synapse.request_type.name.casefold()

def __assert_error_route(synapse_request):
    synapse = MockErrorSynapse(synapse_request)
    resp = synapse.execute()
    print(resp)
    assert resp is not None
    expected = json.loads(resp.body)
    assert expected['error'].casefold() == 'error_str_' + synapse.request_type.name.casefold()

def test_describe_route():
    __assert_route(__get_describe_synapse_request())
    __assert_error_route(__get_describe_synapse_request())

def test_read_synapse_request():
    __assert_route(__get_read_synapse_request())
    __assert_error_route(__get_read_synapse_request())

def test_get_synapse_request():
    request = __get_crud_synapse_request()
    request.type = RequestType.GET
    __assert_route(request.json())
    __assert_error_route(request.json())

def test_create_synapse_request():
    request = __get_crud_synapse_request()
    request.type = RequestType.CREATE
    __assert_route(request.json())
    __assert_error_route(request.json())

def test_update_synapse_request():
    request = __get_crud_synapse_request()
    request.type = RequestType.UPDATE
    __assert_route(request.json())
    __assert_error_route(request.json())

def test_delete_synapse_request():
    request = __get_crud_synapse_request()
    request.type = RequestType.DELETE
    __assert_route(request.json())
    __assert_error_route(request.json())

def test_process_webook_request():
    __assert_route(__get_process_webook_request())
    __assert_error_route(__get_process_webook_request())

def test_invalid_synapse_object():
    with pytest.raises(Exception):
        router = Router(InvalidSynapse())
        resp = router.route()
        assert resp is not None

def test_get_synapse_info():
    synapse_request = Request(type=RequestType.SYNAPSE_INFO,
        connection=get_connection(),
        body=None).json()
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None

def test_connect():
    synapse_request = Request(type=RequestType.CONNECT,
        connection=get_connection(),
        body=None).json()
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    

def get_connection():
    authConfig=AuthConfig(endpoint='http://endpoint.com')
    connection = Connection(id='1', name='name', authConfig=authConfig, idFieldName='idfield', watermarkFieldName='watermarkfield', 
    createdAtFieldName='createdfield', updatedAtFieldName='updatedfield', oAuthRedirectUrl='http://redirect.com')
    return connection
