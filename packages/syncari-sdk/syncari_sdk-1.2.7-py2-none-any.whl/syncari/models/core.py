from enum import Enum
from tokenize import String
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Extra
from syncari.models.schema import DataType

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

class WebhookOperation(str, Enum):
    """
        Identifies all webhook operations
    """ 
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    SYNCARI_DELETE = 'syncari_delete'
    GET = 'get'

class EventData(BaseModel):
    data: Record
    operation: WebhookOperation
    eventId: Optional[str]