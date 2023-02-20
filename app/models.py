
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker, Session, DeclarativeBase
)


DATABASE_URL: str = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Maker: Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


Base.metadata.create_all(bind=engine)
