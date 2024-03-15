import datetime
import typing

import pydantic


class Account(pydantic.BaseModel):
    username: str
    password: str


class Contact(pydantic.BaseModel):
    name: typing.Optional[str] = None
    surname: typing.Optional[str] = None
    birthday: typing.Optional[datetime.date] = None
    email: typing.Optional[str] = None
    phone: typing.Optional[str] = None
