from typing import Optional

import bcrypt
from fastapi import HTTPException, Header
from fastapi.security import HTTPBasic
from jose import jwt

from common.database import get_user_collection
from user_service.api.models import User
from user_service.api.utils.token_utils import SECRET_KEY, ALGORITHM

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


def get_current_user(authorization: str = Header(...)) -> User:
    try:
        token_type, token = authorization.split()
        if token_type != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = decoded_token.get("sub")
        user = get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")




