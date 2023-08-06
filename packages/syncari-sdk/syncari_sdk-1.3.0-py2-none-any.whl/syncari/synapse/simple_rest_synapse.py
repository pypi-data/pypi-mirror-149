from abc import abstractmethod
import json
from enum import Enum
from syncari.models import *
from syncari.rest.client import SyncariRestClient
from syncari.synapse.abstract_synapse import Synapse

class CrudOperation(Enum):
    """
        Identifies all crud operations
    """
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    GET = 'GET'
    DELETE = 'DELETE'

class SimpleRestSynapse(Synapse):
    """
        A simple rest synapse class that implements standard rest methods.
    """

    def __init__(self, request: Request) -> None:
        super().__init__(request)

    def synapse_info(self):
        return super().synapse_info()

    def test(self, connection: Connection):
        return super().test(connection)

    def describe(self, desc_request: DescribeRequest):
        return super().describe(desc_request)

    def read(self, sync_request: SyncRequest):
        return super().read(sync_request)

    def get_by_id(self, sync_request: SyncRequest):
        return self.__crud(CrudOperation.GET, sync_request)

    def create(self, sync_request: SyncRequest):
        return self.__crud(CrudOperation.CREATE, sync_request)

    def update(self, sync_request: SyncRequest):
        return self.__crud(CrudOperation.UPDATE, sync_request)

    def delete(self, sync_request: SyncRequest):
        return self.__crud(CrudOperation.DELETE, sync_request)

    def extract_webhook_identifier(self, webhook_request: WebhookRequest):
        return super().extract_webhook_identifier(webhook_request)

    def process_webhook(self, webhook_request: WebhookRequest):
        return super().process_webhook(webhook_request)

    @abstractmethod
    def get_rest_client(self):
        pass

    def __crud(self, operation, sync_request: SyncRequest):
        entity_name = sync_request.entity.apiName
        plural_name = sync_request.entity.pluralName
        if not plural_name:
            plural_name = entity_name

        rest_client = self.get_rest_client() 
        resps = []
        for data in sync_request.data:
            data = Record.parse_obj(data)
            resp = None
            if operation is CrudOperation.GET:
                resp = rest_client.get(plural_name + "/" + data.id, params=rest_client.auth_config, json=data.values)
            elif operation is CrudOperation.CREATE:
                resp = rest_client.post(plural_name, params=rest_client.auth_config, json=data.values)
            elif operation is CrudOperation.UPDATE:
                resp = rest_client.put(plural_name + "/" + data.id, params=rest_client.auth_config, json=data.values)
            elif operation is CrudOperation.DELETE:
                resp = rest_client.delete(plural_name + "/" + data.id, params=rest_client.auth_config)

            resps.append(resp)
            
        return resps