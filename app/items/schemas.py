from typing import Optional

from pydantic import BaseModel


class ItemBaseSchema(BaseModel):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True


class CreateItemSchema(ItemBaseSchema):
    id: Optional[int]


class UpdateItemSchema(ItemBaseSchema):
    id: Optional[int]
    user_id: Optional[int]
