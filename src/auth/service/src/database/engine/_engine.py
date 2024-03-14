import sqlalchemy
import sqlalchemy.ext.asyncio

import src.database.url


def from_env() -> sqlalchemy.ext.asyncio.AsyncEngine:
    url: sqlalchemy.URL = src.database.url.from_env()
    return sqlalchemy.ext.asyncio.create_async_engine(url)
