from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel
from syncari.models.core import Connection, Record
from syncari.models.schema import Schema

class RequestType(Enum):
    """
        Identifies all types of synapse requests
    """
    SYNAPSE_INFO = 'SYNAPSE_INFO'
    TEST = 'TEST'
    REFRESH_TOKEN = 'REFRESH_TOKEN'
    GET_ACCESS_TOKEN = 'GET_ACCESS_TOKEN'
    DESCRIBE = 'DESCRIBE'
    READ = 'READ'
    GET_BY_ID = 'GET_BY_ID'
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    EXTRACT_WEBHOOK_IDENTIFIER = 'EXTRACT_WEBHOOK_IDENTIFIER'
    PROCESS_WEBHOOK = 'PROCESS_WEBHOOK'

class CrudOperation(Enum):
    """
        Identifies all crud operations
    """
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    GET = 'GET'
    DELETE = 'DELETE'

class OffsetType(str, Enum):
    """
        Denotes the offset type of the read response for this synapse.
    """
    NONE = 'NONE',
    PAGE_NUMBER = 'PAGE_NUMBER',
    RECORD_COUNT = 'RECORD_COUNT',
    TIMESTAMP = 'TIMESTAMP',
    CUSTOM = 'CUSTOM'

class Watermark(BaseModel):
    """
        Represents the incremental watermark information to syncari.
    """
    start: int
    end: int
    offset: Optional[int]
    limit: Optional[int]
    cursor: Optional[str]
    isResync: bool = False
    isTest: bool = False
    initial: bool = False

class Request(BaseModel):
    """
        The request object originating from Syncari framework call to the custom synapse
    """
    type: RequestType
    connection: Connection
    body: Any
    host: Optional[str]
    syncariId: Optional[str]
    requestId: Optional[str]

class ReadResponse(BaseModel):
    """
        The READ  object
    """
    data: Optional[List[Record]]
    watermark: Optional[Watermark]
    offsetType: OffsetType = OffsetType.RECORD_COUNT

class DescribeRequest(BaseModel):
    """
        The describe all request object
    """
    entities: List[str]

class SyncRequest(BaseModel):
    """
        The sync request object
    """
    entity: Schema
    data: Optional[List[Record]]
    watermark: Optional[Watermark]

class WebhookRequest(BaseModel):
    """
        The webhook request object
    """
    body: str
    headers: Optional[dict]
    params: Optional[dict]

class ErrorResponse(BaseModel):
    status_code: int
    detail: Optional[str]
    message: str
        
    class Config:
        """
            allow for object validation workaround
        """
        arbitrary_types_allowed = True