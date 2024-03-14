import os
import pathlib

from src.exceptions import MissingEnvironment


ENV_PEM: str = "OPENSSL_PEM"
ENV_PUB: str = "OPENSSL_PUB"


def read_pem() -> bytes:
    if (path := os.environ.get(ENV_PEM)) is None:
        raise MissingEnvironment(ENV_PEM)
    return pathlib.Path(path).read_bytes()


def read_pub() -> bytes:
    if (path := os.environ.get(ENV_PUB)) is None:
        raise MissingEnvironment(ENV_PUB)
    return pathlib.Path(path).read_bytes()
