from abc import ABC, abstractmethod
import json
from syncari.models import *
from syncari.rest.client import SyncariException
from ..logger import SyncariLogger

# pylint: disable=missing-function-docstring
class Synapse(ABC):
    """
        The abstract synapse class to enforce synapse implementations
    """
    raw_request = None
    connection = None
    request = None
    request_type = None
    init_error = None

    def __init__(self, raw_request: Request) -> None:
        try:
            parsed = Request.parse_raw(self.raw_request)
            self.request_type = parsed.type
            self.connection = parsed.connection
            self.request = self.__set_request(parsed)
        except Exception as e:
            err_msg = 'Failed to execute request {}'.format(raw_request)
            self.init_error = ErrorResponse(message=err_msg, status_code=400, detail=str(e))

    def __set_request(self, parsed: Request):
        if parsed.type == RequestType.DESCRIBE:
            return DescribeRequest.parse_obj(parsed.body)
        elif parsed.type in [RequestType.READ, RequestType.GET_BY_ID, RequestType.CREATE, RequestType.UPDATE, RequestType.DELETE]:
            return SyncRequest.parse_obj(parsed.body)
        elif parsed.type in [RequestType.EXTRACT_WEBHOOK_IDENTIFIER, RequestType.PROCESS_WEBHOOK]:
            return WebhookRequest.parse_obj(parsed.body)
        else:
            return parsed

    def execute(self):
        """
            The route method that looks for the type of the synapse request and invokes
            appropriate synapse supported method.
        """
        # If there is an initialization exception, just return as response. This is needed to capture it as a well defined error.
        if self.init_error is not None:
            return self.init_error

        self.logger.info(self.request_type)
        self.logger.info(self.request)
        response = None
        try:
            if self.request_type == RequestType.TEST:
                response = self.test(self.connection)
                if not isinstance(response, Connection):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.SYNAPSE_INFO:
                response = self.synapse_info()
                if not isinstance(response, SynapseInfo):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.DESCRIBE:
                response = self.describe(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Schema):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.READ:
                response = self.read(self.request)
                if not isinstance(response, ReadResponse):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.GET_BY_ID:
                response = self.get_by_id(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Record):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.CREATE:
                response = self.create(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.UPDATE:
                response = self.update(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.DELETE:
                response = self.delete(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.EXTRACT_WEBHOOK_IDENTIFIER:
                response = self.extract_webhook_identifier(self.request)
                if not isinstance(response, str):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.PROCESS_WEBHOOK:
                response = self.process_webhook(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Record):
                        raise self.__prep_invalid_response_exception(response)

            else:
                self.logger.error(self.request)
                raise Exception('Invalid synapse request {}'.format(self.request_type))

        except SyncariException as e:
            response = e.error_response
            
        except Exception as e:
            err_msg = 'Failed to execute request {}'.format(self.request_type)
            response = ErrorResponse(message=err_msg, status_code=400, detail=str(e))

        if (isinstance(response, list)):
            json_vals = []
            for v in response:
                json_vals.append(v.json())
            return json.dumps(json_vals)

        try:
            json_resp = response.json()
            return json_resp
        except Exception as e:
            self.logger.error('Encountered exception {}'.format(str(e)))
            self.logger.warn('Response was not serializable: {}'.format(response))
            return response

    def __prep_invalid_response_exception(self, response):
        err_msg = 'Invalid response type for request {}'.format(self.request_type)
        detail = 'The response: {}'.format(str(response))
        raise SyncariException(error_response=ErrorResponse(message=err_msg, detail=detail, status_code=400))
        
    @property
    def name(self) -> str:
        """
            Synapse name.
        """
        return self.__class__.__name__

    def print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    @property
    def logger(self):
        return SyncariLogger.get_logger(f"{self.name}")

    @abstractmethod
    def synapse_info(self):
        pass

    @abstractmethod
    def test(self, connection: Connection):
        pass

    @abstractmethod
    def describe(self, desc_request: DescribeRequest):
        pass

    @abstractmethod
    def read(self, sync_request: SyncRequest):
        pass

    @abstractmethod
    def get_by_id(self, sync_request: SyncRequest):
        pass

    @abstractmethod
    def create(self, sync_request: SyncRequest):
        pass

    @abstractmethod
    def update(self, sync_request: SyncRequest):
        pass

    @abstractmethod
    def delete(self, sync_request: SyncRequest):
        pass

    @abstractmethod
    def extract_webhook_identifier(self, webhook_request: WebhookRequest):
        pass

    @abstractmethod
    def process_webhook(self, webhook_request: WebhookRequest):
        pass
