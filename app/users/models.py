from typing import List

import bcrypt
from models import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    _password: Mapped[str] = mapped_column('password', String(50))

    items: Mapped[List['Item']] = relationship('Item', back_populates='user')

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password):
        hashed = bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
        self._password = hashed
