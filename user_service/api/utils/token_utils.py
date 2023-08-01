from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from common.database import get_token_collection
from ..models import User

SECRET_KEY = "1111"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_tokens_for_user(user: User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.email}
    access_token = create_access_token(data=access_token_data, expires_delta=access_token_expires)

    refresh_token_data = {"sub": user.email}
    refresh_token = create_refresh_token(data=refresh_token_data)

    token_data = {
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    get_token_collection().insert_one(token_data)

    return access_token, refresh_token
