import hashlib


def sha256(keyword: str):
    m = hashlib.sha256()
    m.update(keyword.encode())
    return m.hexdigest()
