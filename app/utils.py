
from passlib.context import CryptContext #library for creating hashing path


#using bcrypt as an hashing  algorithm for passwords stored in the database to prevent hackers
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash (password:str):
    return pwd_context.hash(password)
#a verified func to compare the plain passsword attempt then hashing it and compare it to the hashed password in the database 
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
