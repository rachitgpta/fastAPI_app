from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(raw_pwd: str):
    hashed_password = pwd_context.hash(raw_pwd)
    return hashed_password

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
