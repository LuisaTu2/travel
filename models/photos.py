from constants import TRAVELS
from pydantic import BaseModel
from typing import List

from enum import Enum


class TableStatus(str, Enum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"
    INACCESSIBLE_ENCRYPTION_CREDENTIALS = "INACCESSIBLE_ENCRYPTION_CREDENTIALS"
    ARCHIVING = "ARCHIVING"
    ARCHIVED = "ARCHIVED"


class KeyType(str, Enum):
    HASH = "HASH"
    RANGE = "RANGE"


class Item(BaseModel):
    table_name: str
    pk: str
    sk: str


class Photo(Item):
    table_name: str = TRAVELS
    title: str = ""
    description: str = ""
    likes: int = 0
    doggo: int = 0
    mačka: int = 0
    comments: List[str] = []
