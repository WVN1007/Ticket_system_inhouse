# from passlib.context import CryptContext
import bcrypt

# switch from using passlib to bcrypt due to crypt will be deprecated
# scr : https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/

def hash_pwd(pwd: str | bytes):
    if isinstance(pwd,str):
        byte = pwd.encode('utf-8')
    else:
        byte = pwd
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte,salt)
    return hash
