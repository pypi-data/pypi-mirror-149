
# pylint: disable=missing-class-docstring, import-error, missing-function-docstring
import json
from syncari.models import *
from syncari.synapse.abstract_synapse import Synapse

class MockResponseValidationSynapse(Synapse):

    def __print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    def test(self, connection):
        connections = []
        connections.append(connection)
        return connections

    def synapse_info(self):
        return []

    def describe(self, desc_request):
        self.__print(self.describe.__name__, desc_request)
        return Schema.parse_obj({'apiName':'MockSchema','displayName':'MockDisplayName'})

    def read(self, sync_request):
        self.__print(self.read.__name__, sync_request)
        watermark = sync_request.watermark
        return Record.parse_obj({'name':'MockRecord','values':{'key':'val'}})

    def get_by_id(self, sync_request):
        self.__print(self.get_by_id.__name__, sync_request)
        return Record.parse_obj({'name':'MockRecord','values':{'key':'val'}})

    def create(self, sync_request):
        self.__print(self.create.__name__, sync_request)
        return Result.parse_obj({'id':'MockID'})

    def update(self, sync_request):
        self.__print(self.update.__name__, sync_request)
        return Result.parse_obj({'id':'MockID'})

    def delete(self, sync_request):
        self.__print(self.delete.__name__, sync_request)
        return Result.parse_obj({'id':'MockID'})

    def extract_webhook_identifier(self, webhook_request):
        self.__print(self.extract_webhook_identifier.__name__, webhook_request)
        return ['MockWebhookID']

    def process_webhook(self, webhook_request):
        self.__print(self.process_webhook.__name__, webhook_request)
        return Result.parse_obj({'id':'MockID'})

def _execute(synapse_request):
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    err_resp = ErrorResponse.parse_raw(resp)
    return err_resp

def test_connect():
    synapse_request = Request(type=RequestType.TEST,
        connection=get_connection(),
        body=None).json()
    resp = _execute(synapse_request)
    assert isinstance(resp, ErrorResponse)
    assert resp.message == 'Invalid response type for request RequestType.TEST'


def test_get_synapse_info():
    synapse_request = Request(type=RequestType.SYNAPSE_INFO,
        connection=get_connection(),
        body=None).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.SYNAPSE_INFO'
    assert resp.detail == 'The response: []'

def test_describe_route():
    synapse_request = Request(type=RequestType.DESCRIBE,
        connection=get_connection(),
        body=DescribeRequest(entities=['test'])).json()
    synapse = MockResponseValidationSynapse(synapse_request)
    resp = _execute(synapse_request)
    assert resp.message == 'Failed to execute request RequestType.DESCRIBE'
    assert resp.detail == '1 validation error for Schema\nattributes\n  field required (type=value_error.missing)'

def test_read_synapse_request():
    synapse_request = Request(type=RequestType.READ,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    resp = _execute(synapse_request)
    assert resp.message== 'Invalid response type for request RequestType.READ'

def test_get_by_id_synapse_request():
    synapse_request = Request(type=RequestType.GET_BY_ID,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.GET_BY_ID'

def test_create_synapse_request():
    synapse_request = Request(type=RequestType.CREATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.CREATE'

def test_update_synapse_request():
    synapse_request = Request(type=RequestType.UPDATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.UPDATE'

def test_delete_synapse_request():
    synapse_request = Request(type=RequestType.DELETE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.DELETE'

def test_process_webook_request():
    synapse_request = Request(type=RequestType.PROCESS_WEBHOOK,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.PROCESS_WEBHOOK'


def test_extract_webhook_identifier():
    synapse_request = Request(type=RequestType.EXTRACT_WEBHOOK_IDENTIFIER,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    resp = _execute(synapse_request)
    assert resp.message == 'Invalid response type for request RequestType.EXTRACT_WEBHOOK_IDENTIFIER'

def get_connection():
    authConfig=AuthConfig(endpoint='http://endpoint.com')
    connection = Connection(id='1', name='name', authConfig=authConfig, idFieldName='idfield', watermarkFieldName='watermarkfield', 
        endpoint='http://endpoint.com', createdAtFieldName='createdfield', updatedAtFieldName='updatedfield', oAuthRedirectUrl='http://redirect.com')
    return connection
