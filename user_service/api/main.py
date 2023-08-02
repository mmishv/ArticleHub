import atexit
import threading
from datetime import timedelta

import bcrypt
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from jose import jwt

from common.database import get_user_collection, get_token_collection
from user_service.api.article_notifications import listen_to_article_notifications
from .exceptions import UserAlreadyExistsException, InvalidCredentialsException
from .models import User, UserCreate, RefreshTokenInput
from .utils.token_utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    create_tokens_for_user

from .utils.user_utils import get_user_by_email, authenticate_user, get_current_user
from .crud_router import router as user_router
app = FastAPI()

app.include_router(user_router)

notification_thread = threading.Thread(target=listen_to_article_notifications)
notification_thread.start()

atexit.register(notification_thread.join)

@app.post("/register/")
def register_user(user: UserCreate):
    existing_user = get_user_collection().find_one({"email": user.email})
    if existing_user:
        raise UserAlreadyExistsException(user.email)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    password_hash = hashed_password.decode("utf-8")

    user_data = {"email": user.email, "hashed_password": password_hash, "first_name": user.first_name,
                 "last_name": user.last_name, "is_active": True, "is_superuser": False, }

    get_user_collection().insert_one(user_data)

    access_token, refresh_token = create_tokens_for_user(User(**user_data))
    user = User(**user_data)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@app.post("/token/")
def login_for_access_token(refresh_token: RefreshTokenInput):
    try:
        decoded_token = jwt.decode(refresh_token.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
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
def login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise InvalidCredentialsException()

    access_token, refresh_token = create_tokens_for_user(user)
    return {"user": user, "access_token": access_token, "refresh_token": refresh_token}


@app.get("/me/")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/logout/{email}")
def logout(email: str):
    get_token_collection().delete_one({"email": email})
    return {"message": "Successfully logged out"}



