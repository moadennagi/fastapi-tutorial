from typing import List, Union, TypeVar

from models import Base
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.orm import Session


CreateSchema = TypeVar('CreateSchema', bound=BaseModel)


def get_by_id(
    cls: Base,
    session: Session,
    *,
    pk: int
) -> Union[Base, None]:
    "Return a single instance matching the `pk`"
    stmt = select(cls).where(cls.id==pk)
    res = session.execute(stmt).scalar_one()
    return res


def read_all(
    cls: Base,
    session: Session,
    *,
    skip: int = 0,
    limit: int | None = None,
) -> Union[List[Base], List]:
    "Return all rows of `cls`"
    stmt = select(cls).offset(skip)
    if limit:
        stmt = stmt.limit(limit)
    items = session.execute(stmt).scalars().all()
    session.commit()
    return items


def create_one(
    cls: Base,
    session: Session,
    *,
    data: CreateSchema
) -> Base:
    "Create a single instance of `cls`"
    obj = cls(**data.dict(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def update_one(
    session: Session,
    *,
    obj: Base,
    data: CreateSchema
) -> Base:
    "Update the instance the `obj`"
    has_changed = False
    for key, value in data.dict(exclude_unset=True).items():
        if hasattr(obj, key) and getattr(obj, key) != value:
            if isinstance(key) != BaseModel:
                setattr(obj, key, value)
                has_changed = True
    if has_changed:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj


def delete_by_id(
    cls: Base,
    session: Session,
    *,
    pk: int,
) -> Base:
    "Delete and instance of `Base`"
    stmt = delete(cls).where(cls.id==pk).returning(cls.id)
    res = session.execute(stmt)
    session.commit()
    return res