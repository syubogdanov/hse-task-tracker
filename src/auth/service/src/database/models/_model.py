from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func

from src.database.core import DeclarativeBase


class User(DeclarativeBase):
    __tablename__: str = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=False, nullable=False)


class Contact(DeclarativeBase):
    __tablename__: str = "contact"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)
    name = Column(String, unique=False, nullable=True)
    surname = Column(String, unique=False, nullable=True)
    birthday = Column(Date, unique=False, nullable=True)
    email = Column(String, unique=False, nullable=True)
    phone = Column(String, unique=False, nullable=True)

    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        unique=False,
        nullable=False,
    )


class Password(DeclarativeBase):
    __tablename__: str = "password"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user = Column(Integer, ForeignKey(User.id), unique=False, nullable=False)
    md5 = Column(String, unique=False, nullable=False)
    sha256 = Column(String, unique=False, nullable=False)
