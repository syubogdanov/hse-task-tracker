from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import APIKeyCookie

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import AsyncSessionMaker

from src.server.cookie import Cookie


CookieSheme = APIKeyCookie(name=Cookie.cookiename())


async def on_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session


async def on_cookie(token: str = Depends(CookieSheme)) -> AsyncGenerator[Cookie, None]:
    try:
        cookie = Cookie.decode(token)
        assert await cookie.exists()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The cookie is broken or expired",
        )

    yield cookie
