from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"])


def hash_pwd(password: str):
    return context.hash(password)


def serialize(s: str) -> dict:
    d = dict(item.split("=") for item in s.split(","))
    return d


# TODO: switch from using passlib to bcrypt due to crypt will be deprecated
# scr : https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
