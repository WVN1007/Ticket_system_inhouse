from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"])

def hash_pwd(password:str):
    return context.hash(password)
