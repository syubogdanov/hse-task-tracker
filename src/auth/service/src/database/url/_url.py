import os

import sqlalchemy

from src.exceptions import MissingEnvironment


ENV_DIALECT: str = "DATABASE_DIALECT"
ENV_DRIVER: str = "DATABASE_DRIVER"
ENV_USERNAME: str = "DATABASE_USERNAME"
ENV_PASSWORD: str = "DATABASE_PASSWORD"
ENV_HOST: str = "DATABASE_HOST"
ENV_PORT: str = "DATABASE_PORT"
ENV_DATABASE: str = "DATABASE_DATABASE"


def from_env() -> sqlalchemy.URL:
    if (dialect := os.environ.get(ENV_DIALECT)) is None:
        raise MissingEnvironment(ENV_DIALECT)

    if (driver := os.environ.get(ENV_DRIVER)) is None:
        raise MissingEnvironment(ENV_DRIVER)

    if (username := os.environ.get(ENV_USERNAME)) is None:
        raise MissingEnvironment(ENV_USERNAME)

    if (password := os.environ.get(ENV_PASSWORD)) is None:
        raise MissingEnvironment(ENV_PASSWORD)

    if (host := os.environ.get(ENV_HOST)) is None:
        raise MissingEnvironment(ENV_HOST)

    if (port := os.environ.get(ENV_PORT)) is None:
        raise MissingEnvironment(ENV_PORT)

    if (database := os.environ.get(ENV_DATABASE)) is None:
        raise MissingEnvironment(ENV_DATABASE)

    return sqlalchemy.URL.create(
        drivername=f"{dialect}+{driver}",
        username=username,
        password=password,
        host=host,
        port=int(port),
        database=database,
    )
