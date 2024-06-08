from pydantic import BaseModel
from typing import List


class Comment(BaseModel):
    id: str
    photo_id: str
    text: str


class Photo(BaseModel):
    id: str
    description: str
    likes: int
    comments: List[Comment] = []