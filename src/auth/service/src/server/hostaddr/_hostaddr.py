import os

from src.exceptions import MissingEnvironment


ENV_HOST: str = "SERVICE_HOST"
ENV_PORT: str = "SERVICE_PORT"


def from_env() -> tuple[str, int]:
    if (host := os.environ.get(ENV_HOST)) is None:
        raise MissingEnvironment(ENV_HOST)

    if (port := os.environ.get(ENV_PORT)) is None:
        raise MissingEnvironment(ENV_PORT)

    return host, int(port)
