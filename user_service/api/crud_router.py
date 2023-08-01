from typing import List

from fastapi import APIRouter, HTTPException

from user_service.api.crud import create_user, get_user_by_id, get_user_by_email, get_all_users, update_user, \
    delete_user
from user_service.api.models import User

router = APIRouter()


@router.post("/users/", response_model=User)
async def create_user_route(user: User):
    return await create_user(user)


@router.get("/users/{user_id}", response_model=User)
async def get_user_by_id_route(user_id: str):
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/email/{email}", response_model=User)
async def get_users_by_email(email: str):
    user = await get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=List[User])
async def get_all_users_route():
    return await get_all_users()


@router.put("/users/{user_id}", response_model=User)
async def update_user_route(user_id: str, updated_data: dict):
    user = await update_user(user_id, updated_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user_route(user_id: str):
    if not await delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
