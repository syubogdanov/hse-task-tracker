import uvicorn

from src.server.api import API
from src.server import addr


def main() -> None:
    host, port = addr.from_env()
    uvicorn.run(
        app=API,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()
