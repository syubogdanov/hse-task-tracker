from __future__ import annotations

import jwt
import pydantic

from src.database.models import User
from src.database.session import AsyncSessionMaker
from src.database.repository import Repository
from src.security import openssl


RSA256 = "RS256"


class Cookie(pydantic.BaseModel):
    username: str

    def encode(self) -> str:
        payload = self.model_dump_json()
        return jwt.encode(payload, openssl.read_pem(), RSA256)

    @staticmethod
    def decode(token: str) -> Cookie:
        payload = jwt.decode(token, openssl.read_pub(), RSA256)
        return Cookie(**payload)

    async def ok(self) -> bool:
        with AsyncSessionMaker() as session:
            condition = (User.username == self.username)
            return await Repository(User, session).exists(condition)
