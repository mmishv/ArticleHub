from bson import ObjectId
from starlette.testclient import TestClient

from common.database import USER_COLLECTION_NAME
from common.settings import BASE_URL
from user_service.api.main import app
from user_service.api.models import User


client = TestClient(app, base_url=BASE_URL)

user_data = {"email": "test@example.com",
             "hashed_password": "testpassword",
             "first_name": "John",
             "last_name": "Doe",
             "is_active": True,
             "is_superuser": False, }

user = User(**user_data)


def test_create_user(db):
    response = client.post("/users/", json=user.model_dump())

    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name

    created_user = db[USER_COLLECTION_NAME].find_one({"email": user.email})
    assert created_user is not None


def test_get_user_by_id(db):
    result = db[USER_COLLECTION_NAME].insert_one(user.model_dump())
    user_id = str(result.inserted_id)

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    assert response.json()["email"] == user.email
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name


def test_get_user_by_email(db):
    db[USER_COLLECTION_NAME].insert_one(user.model_dump())

    response = client.get(f"/users/email/{user.email}")

    assert response.status_code == 200

    assert response.json()["email"] == user.email
    assert response.json()["first_name"] == user.first_name
    assert response.json()["last_name"] == user.last_name


def test_get_all_users(db):
    global user
    test_users = [user.model_dump(), ]
    for item in test_users:
        db[USER_COLLECTION_NAME].insert_one(item)

    users = client.get("/users/")

    assert users.status_code == 200


def test_update_user(db):
    result = db[USER_COLLECTION_NAME].insert_one(user.model_dump())
    user_id = str(result.inserted_id)

    updated_data = {"first_name": "Updated", "last_name": "User"}

    response = client.put(f"/users/{user_id}", json=updated_data)

    assert response.status_code == 200

    assert response.json()["first_name"] == updated_data["first_name"]
    assert response.json()["last_name"] == updated_data["last_name"]


def test_delete_user(db):
    result = db[USER_COLLECTION_NAME].insert_one(user.model_dump())
    user_id = str(result.inserted_id)

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200

    deleted_user = db[USER_COLLECTION_NAME].find_one({"_id": ObjectId(user_id)})
    assert deleted_user is None
