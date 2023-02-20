from typing import Optional, List
from items.schemas import ItemBaseSchema
from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    id: int
    username: str
    password: str
    items: List['ItemBaseSchema']


class UserCreateSchema(UserSchemaBase):
    id: Optional[int]
    username: str
    password: str
    items: Optional[List['ItemBaseSchema']]
