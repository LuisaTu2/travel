from typing import List

from models.db import Item


class Photo(Item):
    title: str = ""
    description: str = ""
    likes: int = 0
    doggo: int = 0
    macka: int = 0
    comments: List[str] = []
