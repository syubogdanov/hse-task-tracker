import sqlalchemy

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Response
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.database.models import Password
from src.database.models import User

from src.security import md5
from src.security import sha256

from src.server.cookie import Cookie

from src.server.dependency import on_cookie
from src.server.dependency import on_session

from src.server.schemas import Account as AccountScheme
from src.server.schemas import Contact as ContactScheme


API = FastAPI()


@API.post("/signup")
async def on_signup(
    account: AccountScheme,
    session: AsyncSession = Depends(on_session),
) -> Response:
    """
    Creates a new user in the task tracker

    Args:
    - `username`: the username that will be used in the system
    - `password`: the password that will be associated with the user

    Status:
    - `201`: the user has been successfully created
    - `409`: the username is already taken

    Headers:
    - `Set-Cookie`: the token for future authorization
    """
    query = sqlalchemy.select(
        sqlalchemy.select(User)
        .where(User.username == account.username)
        .exists()
    )

    if (await session.scalar(query)):
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
    tag: str = Cookie.cookiename()
    token: str = cookie.encode()

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Set-Cookie": f"{tag}={token}"},
    )


@API.post("/login")
async def on_login(
    account: AccountScheme,
    session: AsyncSession = Depends(on_session),
) -> Response:
    """
    Authorizes in the task tracker

    Args:
    - `username`: the username that is used in the system
    - `password`: the password that is associated with the user

    Status:
    - `200`: OK
    - `403`: the password is incorrect
    - `404`: the user does not exist

    Headers:
    - `Set-Cookie`: the cookie for future authorization
    """
    query = (
        sqlalchemy.select(User)
        .where(User.username == account.username)
    )

    if not (user := await session.scalar(query)):
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    password = await session.scalar(
        sqlalchemy.select(Password)
        .where(Password.user == user.id)
    )

    if password.md5 != md5.upass(account.username, account.password):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    if password.sha256 != sha256.upass(account.username, account.password):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    cookie = Cookie(username=account.username)
    tag: str = Cookie.cookiename()
    token: str = cookie.encode()

    return Response(
        status_code=status.HTTP_200_OK,
        headers={"Set-Cookie": f"{tag}={token}"},
    )


@API.patch("/update")
async def on_update(
    contact: ContactScheme,
    cookie: Cookie = Depends(on_cookie),
    session: AsyncSession = Depends(on_session),
) -> Response:
    """
    Updates the user personal information

    Args:
    - `name`: the user's name
    - `surname`: the user's surname
    - `bithday`: the user's birthday
    - `email`: the user's email address
    - `phone`: the user's mobile phone number

    Status:
    - `200`: OK
    - `400`: the data is empty

    Note:
    - Requires the authorization cookie
    """
    updates = {
        key: value
        for key, value in contact.model_dump().items()
        if value is not None
    }

    if not updates:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user = await session.scalar(
        sqlalchemy.select(User)
        .where(User.username == cookie.username)
    )

    await session.execute(
        sqlalchemy.update(Contact)
        .where(Contact.user == user.id)
        .values(updates)
    )

    await session.commit()

    return Response(status_code=status.HTTP_200_OK)


@API.get("/healthcheck")
async def on_healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)
