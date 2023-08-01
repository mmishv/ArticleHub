from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from common.database import get_user_collection
from user_service.api.models import User

security = HTTPBasic()


def get_user_by_email(email: str) -> Optional[User]:
    user_data = get_user_collection().find_one({"email": email})
    if user_data:
        user = User(**user_data)
        return user
    else:
        return None


def authenticate_user(email: str, password: str) -> Optional[User]:
    user_data = get_user_collection().find_one({"email": email})
    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data["hashed_password"].encode('utf-8')):
        user = User(**user_data)
        return user
    return None


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> Optional[User]:
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user




