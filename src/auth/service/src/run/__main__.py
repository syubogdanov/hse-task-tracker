import uvicorn

from src.server.api import API
from src.server import hostaddr


def main() -> None:
    host, port = hostaddr.from_env()
    uvicorn.run(
        app=API,
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()
