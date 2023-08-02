from datetime import timedelta

from jose import jwt
from starlette.testclient import TestClient

from common.database import USER_COLLECTION_NAME
from common.settings import USER_BASE_URL
from user_service.api.main import app
from user_service.api.models import UserCreate, User
from user_service.api.utils.token_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, SECRET_KEY, ALGORITHM

client = TestClient(app, base_url=USER_BASE_URL)

user_data = {"email": "test@example.com",
             "hashed_password": "testpassword",
             "first_name": "Test",
             "last_name": "User",
             "is_active": True,
             "is_superuser": False}

create_user_data = {"email": user_data.get('email'),
                    "password": user_data.get('hashed_password'),
                    "first_name": user_data.get('first_name'),
                    "last_name": user_data.get('last_name')}

user = User(**user_data)
create_user = UserCreate(**create_user_data)


def test_register_user(db):
    response = client.post("/register/", json=create_user.model_dump())

    assert response.status_code == 200

    assert response.json().get('user').get("email") == create_user_data.get('email')
    assert response.json().get('user').get("first_name") == create_user_data.get('first_name')
    assert response.json().get('user').get("last_name") == create_user_data.get('last_name')

    new_user = db[USER_COLLECTION_NAME].find_one({"email": create_user_data["email"]})
    assert new_user is not None


def test_register_existing_user():
    client.post("/register/", json=create_user.model_dump())
    second_response = client.post("/register/", json=create_user.model_dump())
    assert second_response.status_code == 400


def test_login_for_access_token(db):
    client.post("/register/", json=create_user.model_dump())

    refresh_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_data = {"sub": "test@example.com"}
    refresh_token = create_access_token(data=refresh_token_data, expires_delta=refresh_token_expires)

    response = client.post("/token/", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    access_token = data["access_token"]

    decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "test@example.com"


def test_login(db):
    client.post("/register/", json=create_user.model_dump())
    response = client.post("/login/", auth=("test@example.com", "testpassword"))

    assert response.status_code == 200

    data = response.json()
    assert "user" in data
    assert "access_token" in data
    assert "refresh_token" in data


def test_read_users_me(db):
    access_token = client.post("/register/", json=create_user.model_dump()).json()['access_token']
    response = client.get("/me/", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    data = response.json()
    assert "email" in data
    assert data["email"] == "test@example.com"
    assert "first_name" in data
    assert data["first_name"] == "Test"
    assert "last_name" in data
    assert data["last_name"] == "User"


def test_logout(db):
    client.post("/register/", json=create_user.model_dump())
    response = client.post("/logout/test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Successfully logged out"
