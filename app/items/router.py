from typing import List

import crud
from dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from items.models import Item
from items.schemas import CreateItemSchema, ItemBaseSchema, UpdateItemSchema
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    '',
    response_model=List[ItemBaseSchema]
)
def read_items(
    session: Session = Depends(get_session),
    skip: int = 0, limit: int | None = None
) -> List[ItemBaseSchema]:
    items = crud.read_all(Item, session, skip=skip, limit=limit)
    return items


@router.post('/')
def create(
    data: CreateItemSchema,
    session: Session = Depends(get_session)
) -> ItemBaseSchema:
    res = crud.create_one(Item, session, data=data)
    return res


@router.put('/{item_id}')
def update(
    item_id: int,
    update_data: UpdateItemSchema,
    session: Session = Depends(get_session)
) -> ItemBaseSchema:
    try:
        item = crud.get_by_id(Item, session, pk=item_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Not found')
    res = crud.update_one(session, obj=item, data=update_data)
    return res


@router.delete('/{item_id}')
def delete(
    item_id: int,
    session: Session = Depends(get_session)
) -> ItemBaseSchema:
    try:
        item = crud.get_by_id(Item, session, item_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Not found')
    crud.delete_by_id(Item, session, pk=item_id)
    return item
