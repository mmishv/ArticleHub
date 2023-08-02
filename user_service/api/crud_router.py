from typing import List

from fastapi import APIRouter, HTTPException

from user_service.api.crud import create_user, get_user_by_id, get_user_by_email, get_all_users, update_user, \
    delete_user
from user_service.api.models import User

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user_route(user: User):
    return create_user(user)


@router.get("/users/{user_id}", response_model=User)
def get_user_by_id_route(user_id: str):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/email/{email}", response_model=User)
def get_users_by_email(email: str):
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=List[User])
def get_all_users_route():
    return get_all_users()


@router.put("/users/{user_id}", response_model=User)
def update_user_route(user_id: str, updated_data: dict):
    user = update_user(user_id, updated_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
def delete_user_route(user_id: str):
    if not delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
