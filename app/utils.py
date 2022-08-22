from passlib.context import CryptContext


def hash(raw_pwd: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
    hashed_password = pwd_context.hash(raw_pwd)
    return hashed_password
