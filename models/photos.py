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


class Comment(BaseModel):
    id: str
    photo_id: str
    text: str


class Item(BaseModel):
    pk: str
    sk: str
    title: str
    description: str
    likes: int = 0
    comments: List[Comment] = []
