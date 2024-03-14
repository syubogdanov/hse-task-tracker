import sqlalchemy.ext.asyncio

import src.database.engine


AsyncSessionMaker = sqlalchemy.ext.asyncio.async_sessionmaker(
    bind=src.database.engine.from_env(),
    autoflush=False,
)
