from datetime import timedelta

import bcrypt
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from jose import jwt

from common.database import users_collection, tokens_collection
from .exceptions import UserAlreadyExistsException, InvalidCredentialsException
from .models import User, UserCreate
from .utils.token_utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    create_tokens_for_user

from .utils.user_utils import get_user_by_email, authenticate_user

app = FastAPI()


@app.post("/register/")
async def register_user(user: UserCreate):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise UserAlreadyExistsException(user.email)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    password_hash = hashed_password.decode("utf-8")

    user_data = {"email": user.email, "hashed_password": password_hash, "first_name": user.first_name,
                 "last_name": user.last_name, "is_active": True, "is_superuser": False, }

    users_collection.insert_one(user_data)

    access_token, refresh_token = create_tokens_for_user(User(**user_data))
    user = User(**user_data)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@app.post("/token/")
async def login_for_access_token(refresh_token: str):
    try:
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        raise InvalidCredentialsException()

    email = decoded_token.get("sub")
    user = get_user_by_email(email)

    if not user:
        raise InvalidCredentialsException()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.email}
    access_token = create_access_token(data=access_token_data, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login/")
async def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise InvalidCredentialsException()

    access_token, refresh_token = create_tokens_for_user(user)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@app.get("/me/")
async def read_users_me(current_user: User = Depends(get_user_by_email)):
    return current_user


@app.post("/logout/")
async def logout(email: str):
    tokens_collection.delete_one({"email": email})
    return {"message": "Successfully logged out"}
