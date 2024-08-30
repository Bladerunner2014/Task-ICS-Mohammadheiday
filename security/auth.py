import time
from dotenv import dotenv_values
from jose import jwt

from fastapi import Request, HTTPException, Depends, status
from typing import Annotated

from pydantic import BaseModel

from constants.error_message import ErrorMessage

config = dotenv_values(".env")

class TokenPayload(BaseModel):
    is_authenticated: bool = False
    phone: str = None
    role: str = None


def verify_authorization_header(authorization: str) -> str:
    try:
        token_type, token = authorization.split()
    except ValueError:
        raise HTTPException(detail=ErrorMessage.INVALID_TOKEN_FORMAT,
                            status_code=status.HTTP_401_UNAUTHORIZED)

    if token_type != "Bearer":
        raise HTTPException(detail=ErrorMessage.INVALID_TOKEN,
                            status_code=status.HTTP_401_UNAUTHORIZED)

    return token


def decode_jwt_token(token) -> dict:
    try:
        decoded_token = jwt.decode(token=token, key=config["SECRET_KEY"], algorithms=config["ALGORITHM"])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail=ErrorMessage.INVALID_TOKEN_EXPIRED,
                            status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.JWTError:
        raise HTTPException(detail=ErrorMessage.INVALID_TOKEN,
                            status_code=status.HTTP_401_UNAUTHORIZED)


def get_token_payload(token: str) -> TokenPayload:
    decoded_token = decode_jwt_token(token)
    payload = TokenPayload(
        is_authenticated=True,
        role=decoded_token.get("user_role"),
        phone=decoded_token.get("user_phone")
    )
    return payload


def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(detail=ErrorMessage.AUTHENTICATION_REQUIRED,
                            status_code=status.HTTP_401_UNAUTHORIZED)

    token = verify_authorization_header(authorization)
    user = get_token_payload(token=token)
    return user


CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
