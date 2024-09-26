# from passlib.context import CryptContext
import bcrypt

# context = CryptContext(schemes=["bcrypt"])


# def hash_pwd(password: str):
#     return context.hash(password)

# TODO: switch from using passlib to bcrypt due to crypt will be deprecated
# scr : https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

def hash_pwd(pwd: str):
    byte = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte,salt)
    return hash
