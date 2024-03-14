class MissingEnvironment(KeyError):
    def __init__(self, key: str) -> None:
        super().__init__(f"The environment variable {key} is not set")
