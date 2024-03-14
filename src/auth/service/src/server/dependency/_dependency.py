from collections.abc import AsyncGenerator
from collections.abc import Callable

from typing import TypeVar
from typing import Type

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import DeclarativeBase
from src.database.repository import Repository
from src.database.session import AsyncSessionMaker


Model = TypeVar("Model", bound=DeclarativeBase)


async def on_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as async_session:
        yield async_session


def on_repository(prototype: Type[Model]) -> Callable[[AsyncSession], Repository[Model]]:
    def dependency(session: AsyncSession = Depends(on_session)) -> Repository[Model]:
        return Repository(prototype, session)
    return dependency
