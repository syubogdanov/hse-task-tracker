import functools

from collections.abc import Callable

from typing import Any
from typing import TypeVar
from typing import Type

import jwt

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Response
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Password
from src.database.models import User
from src.database.repository import Repository

from src.security import md5
from src.security import openssl
from src.security import sha256

from src.server.cookie import Cookie

from src.server.dependency import on_repository
from src.server.dependency import on_session

from src.server.schemas import Account as AccountScheme
from src.server.schemas import Contact as ContactScheme


COOKIE: str = "jwt"


API = FastAPI()


@API.post("/api/v1/signup")
async def on_signup(
    account: AccountScheme,
    session: AsyncSession = Depends(on_session),
) -> Response:
    condition = User.username == account.username
    if await Repository(User, session).exists(condition):
        return Response(status_code=status.HTTP_409_CONFLICT)

    user = User(username=account.username)

    session.add(user)
    await session.flush()

    session.add(Password(
        user=user.id,
        md5=md5.upass(
            account.username,
            account.password,
        ),
        sha256=sha256.upass(
            account.username,
            account.password,
        ),
    ))

    await session.flush()
    await session.commit()

    cookie = Cookie(username=account.username)
    token: str = cookie.encode()

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Set-Cookie": f"{COOKIE}={token}"},
    )


@API.post("/api/v1/login")
async def on_login(
    account: AccountScheme,
    session: AsyncSession = Depends(on_session),
) -> Response:
    repository = Repository(User, session)
    condition = User.username == account.username

    if not await repository.exists(condition):
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    user: User = await repository.one(condition)

    condition = (Password.user == user.id)
    password: Password = await Repository(Password, session).one(condition)

    if password.md5 != md5.upass(account.username, account.password):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if password.sha256 != sha256.upass(account.username, account.password):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    cookie = Cookie(username=account.username)
    token: str = cookie.encode()

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Set-Cookie": f"{COOKIE}={token}"},
    )


@API.patch("/api/v1/update")
async def on_update(contact: ContactScheme) -> Response:
    ...


@API.get("/api/v1/healthcheck")
async def on_healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)
