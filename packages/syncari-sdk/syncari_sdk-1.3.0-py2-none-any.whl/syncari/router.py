from syncari.models.request import (DescribeRequest,
    SyncRequest, WebhookRequest, RequestType)

from syncari.synapse.abstract_synapse import Synapse
from .logger import SyncariLogger

logger = SyncariLogger.get_logger('syncari')

class Router():
    """
        The router that would route the incoming synapse request to specific route types
        supported by a synapse.
    """

    def __init__(self, synapse: Synapse) -> None:
        """
            Constructor of router
        """
        self.synapse = synapse

    def route(self):
        """
            The route method that looks for the type of the synapse request and invokes
            appropriate synapse supported method.
        """
        request = self.synapse.request
        logger.info(request)
        response = None
        if request.type == RequestType.INIT:
            response = self.synapse.init()
        elif request.type == RequestType.SYNAPSE_INFO:
            response = self.synapse.synapse_info()
        elif request.type == RequestType.DESCRIBE:
            self.synapse.request.body = DescribeRequest.parse_obj(request.body)
            response = self.synapse.describe()
        elif request.type == RequestType.READ:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.read()
        elif request.type == RequestType.GET:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.get()
        elif request.type == RequestType.CREATE:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.create()
        elif request.type == RequestType.UPDATE:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.update()
        elif request.type == RequestType.DELETE:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.delete()
        elif request.type == RequestType.EXTRACT_WEBHOOK_IDENTIFIER:
            self.synapse.request.body = WebhookRequest.parse_obj(request.body)
            response = self.synapse.extract_webhook_identifier()
        elif request.type == RequestType.PROCESS_WEBHOOK:
            self.synapse.request.body = WebhookRequest.parse_obj(request.body)
            response = self.synapse.process_webhook()
        else:
            self.synapse.request.body = SyncRequest.parse_obj(request.body)
            response = self.synapse.read()


        return response
