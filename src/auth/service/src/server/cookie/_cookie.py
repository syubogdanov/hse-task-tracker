from __future__ import annotations

import typing

import jwt
import pydantic
import sqlalchemy

from src.database.models import User
from src.database.session import AsyncSessionMaker

from src.security import openssl


RSA256: str = "RS256"


class Cookie(pydantic.BaseModel):
    username: str

    async def exists(self) -> bool:
        query = sqlalchemy.select(
            sqlalchemy.select(User)
            .where(User.username == self.username)
            .exists()
        )

        async with AsyncSessionMaker() as session:
            return await session.scalar(query)

    def encode(self) -> str:
        return jwt.encode(self.model_dump(), openssl.read_pem(), RSA256)

    @staticmethod
    def decode(token: str) -> Cookie:
        return Cookie(**jwt.decode(token, openssl.read_pub(), [RSA256]))

    @classmethod
    def cookiename(cls: typing.Type[Cookie]) -> str:
        return "cookie"
