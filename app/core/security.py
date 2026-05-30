from passlib.context import CryptContext
import hashlib

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_content.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_content.verify(plain_password, hashed_password)

