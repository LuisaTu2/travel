from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


# DynamoDB models

class KeyType(str, Enum):
    HASH = "HASH"
    RANGE = "RANGE"


class AttributeType(str, Enum):
    S = "S"
    N = "N"
    B = "B"


class BillingMode(str, Enum):
    PROVISIONED = "PROVISIONED"
    PAY_PER_REQUEST = "PAY_PER_REQUEST"


class AttributeName(TypedDict):
    AttributeName: str


class AttributeDefinition(AttributeName):
    AttributeType: AttributeType


class KeySchemaElement(AttributeName):
    KeyType: KeyType


class CreateTableRequest(BaseModel):
    attribute_definitions: List[AttributeDefinition]
    table_name: str
    key_schema: List[KeySchemaElement]
    billing_mode: BillingMode


class Item(BaseModel):
    pk: str
    sk: str


class Key(TypedDict):
    pk: str
    sk: str = ""


class UpdateItemRequest(BaseModel):
    key: Key
    update_expression: str
    expression_attribute_values: Optional[dict] = None


class TableStatus(str, Enum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"
    INACCESSIBLE_ENCRYPTION_CREDENTIALS = "INACCESSIBLE_ENCRYPTION_CREDENTIALS"
    ARCHIVING = "ARCHIVING"
    ARCHIVED = "ARCHIVED"


# travels table models

class Photo(Item):
    title: str = ""
    description: str = ""
    link: str = ""
    likes: int = 0
    doggo: int = 0
    macka: int = 0
    comments: List[str] = []


class Action(str, Enum):
    INCREMENT_REACTION = "INCREMENT_REACTION"
    ADD_COMMENT = "ADD_COMMENT"
    DELETE_COMMENT = "DELETE_COMMENT"


class Reaction(str, Enum):
    LIKE = "like"
    DOGGO = "doggo"
    MACKA = "macka"


class UpdatePhotoRequest(BaseModel):
    key: Key
    action: Action
    reaction: Optional[Reaction] = None
    comment: Optional[str] = None
    position: Optional[int] = None