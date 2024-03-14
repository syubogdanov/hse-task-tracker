from typing import Any
from typing import Generic
from typing import TypeVar
from typing import Type

import sqlalchemy

from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import DeclarativeBase


Model = TypeVar("Model", bound=DeclarativeBase)


class Repository(Generic[Model]):
    __slots__: tuple[str] = (
        "_prototype",
        "_session",
    )

    def __init__(self, prototype: Type[Model], session: AsyncSession) -> None:
        self._prototype: Type[Model] = prototype
        self._session: AsyncSession = session

    async def add(self, **attributes: Any) -> Model:
        model = self._prototype(**attributes)
        self._session.add(model)

        await self._session.commit()
        await self._session.refresh(model)

        return model

    async def filter(self, *criteria: ColumnExpressionArgument) -> list[Model]:
        select = sqlalchemy.select(self._prototype)

        if criteria:
            select = select.filter(*criteria)

        return list(await self._session.scalars(select))

    async def where(self, *criteria: ColumnExpressionArgument) -> list[Model]:
        return (await self.filter(*criteria))

    async def one(self, *criteria: ColumnExpressionArgument) -> Model:
        # TODO: Assert Being Single
        # TODO: Build Another Query

        models = await self.filter(*criteria)
        return models[0]

    async def exists(self, *criteria: ColumnExpressionArgument) -> bool:
        exists = sqlalchemy.select(self._prototype)

        if criteria:
            exists = exists.filter(*criteria)

        exists = exists.exists()
        select = sqlalchemy.select(self._prototype).where(exists)

        return (await self._session.scalar(select)) is not None
