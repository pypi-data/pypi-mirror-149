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
    rest_client = None

    def __init__(self, request: Request, id_field: str, response_path: str) -> None:
        super().__init__(request)
        self.id_field = id_field
        self.response_path = response_path

    def synapse_info(self):
        return super().synapse_info()

    def test(self):
        return super().test()

    def describe(self):
        return super().describe()

    def read(self):
        return super().read()

    def get_by_id(self):
        return self.__crud(CrudOperation.GET)

    def create(self):
        return self.__crud(CrudOperation.CREATE)

    def update(self):
        return self.__crud(CrudOperation.UPDATE)

    def delete(self):
        return self.__crud(CrudOperation.DELETE)

    def extract_webhook_identifier(self):
        return super().extract_webhook_identifier()

    def process_webhook(self):
        return super().process_webhook()

    @abstractmethod
    def process_single_row(self):
        pass

    def get_rest_client(self):
        self.rest_client = SyncariRestClient(self.connection.endpoint, {'api_token':self.connection.authConfig.accessToken})
        return self.rest_client

    def __crud(self, operation):
        entity_name = self.request.entity.apiName
        plural_name = self.request.entity.pluralName
        if not plural_name:
            plural_name = entity_name

        super().print(self.get_by_id.__name__, self.request)
        rest_client = self.get_rest_client() 
        eds = []
        for data in self.request.data:
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

            if type(resp) is ErrorResponse:
                eds.append(Result(id=data.id,syncariId=data.syncariEntityId,success=False,errors=[str(resp)]))

            elif self.response_path in resp.json():
                row = resp.json()[self.response_path]
                if operation is CrudOperation.GET:
                    eds.append(self.process_single_row(entity_name, self.request.entity, row))
                else:
                    id_val = data.id
                    if row is not None and isinstance(row, dict) and self.id_field in row:
                        id_val = row[self.id_field]
                    eds.append(Result(id=id_val,syncariId=data.syncariEntityId,success=True))
            
        return eds

    