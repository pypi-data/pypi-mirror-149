from datetime import datetime
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Extra

class DataType(Enum):
    """
        Identifies the various datatypes supported by Syncari attributes.
    """
    BOOLEAN = 'boolean'
    DECIMAL = 'decimal'
    DOUBLE = 'double'
    REFERENCE = 'reference'
    PICKLIST = 'picklist'
    STRING = 'string'
    DATETIME = 'datetime'
    TIMESTAMP = 'timestamp'
    INTEGER = 'integer'
    DATE = 'date'
    OBJECT = 'object'
    CHILD = 'child'
    PASSWORD = 'password'

class Status(Enum):
    """
        The status of the entity/attribute schema.
    """
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    DELETED = 'DELETED'
    PENDING = 'PENDING'

class Attribute(BaseModel):
    """
        Represents the schema for one attribute within an entity.
    """
    id: Optional[str]
    apiName: str
    displayName: str
    dataType: DataType = DataType.STRING
    custom: bool = False
    defaultValue: Optional[str]
    nillable: bool = True
    initializable: bool = True
    updateable: bool = True
    createOnly: bool = False
    calculated: bool = False
    unique: bool = False
    length: Optional[int]
    precision: Optional[int]
    scale: Optional[int]
    status: Status = Status.ACTIVE
    referenceTo: Optional[str]
    referenceTargetField: Optional[str]
    referenceToPluralName: Optional[str]
    isSystem: bool = False
    isIdField: bool = False
    compositeKey: Optional[str]
    isWatermarkField: bool = False
    isCreatedAtField: bool = False
    isUpdatedAtField: bool = False
    isMultiValueField: bool = False
    isSyncariDefined: bool = False
    parentAttributeId: Optional[str]
    externalId: Optional[str]
    entityId: Optional[str]
    picklistValues: Optional[List[str]]

class Schema(BaseModel):
    """
        Represents the schema for one entity.
    """
    id: Optional[str]
    apiName: str
    displayName: str
    pluralName: Optional[str]
    description: Optional[str]
    custom: bool = False
    readOnly: bool = False
    version: Optional[int]
    child: bool = False
    attributes: List[Attribute]

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

class OffsetType(str, Enum):
    """
        Denotes the offset type of the read response for this synapse.
    """
    NONE = 'NONE',
    PAGE_NUMBER = 'PAGE_NUMBER',
    RECORD_COUNT = 'RECORD_COUNT',
    TIMESTAMP = 'TIMESTAMP'

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

class AuthType(Enum):
    """
        Identifies all auth types
    """
    BASIC_TOKEN = 'UserPasswordToken'
    USER_PWD = 'UserPassword'
    API_KEY = 'ApiKey'
    OAUTH = 'Oauth'
    SIMPLE_OAUTH = 'SimpleOAuth'

class AuthField(BaseModel):
    """
        Represents an auth field.
    """
    name: str
    dataType: DataType = DataType.STRING
    label: Optional[str]
    required: bool = True

class AuthMetadata(BaseModel):
    """
        Represents an authentication mechanism metadata
    """
    authType: AuthType
    fields: Optional[List[AuthField]]
    label: Optional[str]

# TBD This may not be needed.
class UIMetadata(BaseModel):
    """
        Represents an UI Metadata
    """
    displayName: str
    iconPath: Optional[str]
    backgroundColor: Optional[str]

class SynapseInfo(BaseModel):
    """
        Synapse information representation.
    """
    name: str
    category: str
    metadata: UIMetadata
    supportedAuthTypes: List[AuthMetadata]
    configuredFields: Optional[List[AuthField]]
    disabledMessage: Optional[str]

class AuthConfig(BaseModel):
    """
        The authentication configuration for auth mechanism.
    """
    endpoint: Optional[str]
    userName: Optional[str]
    password: Optional[str]
    clientId: Optional[str]
    clientSecret: Optional[str]
    redirectUri: Optional[str]
    token: Optional[str]
    accessToken: Optional[str]
    refreshToken: Optional[str]
    expiresIn: Optional[str]
    lastRefreshed: Optional[datetime]
    additionalHeaders: Optional[dict[str, str]]

class Connection(BaseModel):
    """
        The connection information object.
    """
    name: str
    authConfig: AuthConfig
    idFieldName: Optional[str]
    watermarkFieldName: Optional[str]
    createdAtFieldName: Optional[str]
    updatedAtFieldName: Optional[str]
    oAuthRedirectUrl: Optional[str]
    metaConfig: Optional[dict[str, object]]

    class Config:
        """
            allow for object validation workaround
        """
        arbitrary_types_allowed = True
        extra = Extra.allow

class Record(BaseModel):
    """
        Represents a syncari record.
    """
    name: Optional[str]
    id: Optional[str]
    syncariEntityId: Optional[str]
    deleted: bool = False
    values: dict[str, object]
    lastModified: Optional[int]
    createdAt: Optional[int]

    class Config:
        """
            allow for object validation workaround
        """
        arbitrary_types_allowed = True

class Result(BaseModel):
    """
        Represents a single CRUD operation result.
    """
    success: bool = True
    errors: Optional[List[str]]
    id: Optional[str]
    syncariId: Optional[str]

class InitConnectionInfo(BaseModel):
    """
        Synapse connection initialization info response.
    """
    connection: Connection
    message: Optional[str]
    code: Optional[str]
    errors: Optional[List[str]]
    metaConfig: Optional[dict]

class Request(BaseModel):
    """
        The request object originating from Syncari framework call to the custom synapse
    """
    type: RequestType
    connection: Connection
    body: Any

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