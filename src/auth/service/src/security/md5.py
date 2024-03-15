import hashlib


def encode(string: str) -> str:
    return hashlib.md5(string.encode()).hexdigest()


def upass(username: str, password: str) -> str:
    return encode(f"{username} % {encode(password)}")
