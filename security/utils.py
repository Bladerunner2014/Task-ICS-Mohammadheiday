from datetime import timedelta, timezone, datetime
from typing import Optional
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder
from jose import jwt
from passlib.context import CryptContext

from schemas.schema import TokenPayload
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = dotenv_values(".env")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)
def create_access_token(subject: TokenPayload, expires_duration: Optional[int] = None) -> str:
    if expires_duration:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_duration)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)

    to_encode = jsonable_encoder(subject.model_dump())
    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return encoded_jwt
