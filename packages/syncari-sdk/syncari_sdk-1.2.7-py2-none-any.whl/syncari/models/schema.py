from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class DataType(Enum):
    """
        Identifies the various datatypes supported by Syncari attributes.
    """
    BOOLEAN = 'boolean'
    DECIMAL = 'decimal'
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
