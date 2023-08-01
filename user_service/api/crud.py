from bson import ObjectId
from typing import Optional, List

from common.database import get_user_collection, get_database
from .models import User


async def create_user(user: User, ) -> User:
    user_data = {
        "email": user.email,
        "hashed_password": user.hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }
    get_database()["users"].insert_one(user_data)
    return user


async def get_user_by_id(user_id: str) -> Optional[User]:
    user_data = get_user_collection().find_one({"_id": ObjectId(user_id)})
    if user_data:
        user = User(**user_data)
        return user
    else:
        return None


async def get_user_by_email(email: str) -> Optional[User]:
    user_data = get_user_collection().find_one({"email": email})
    if user_data:
        user = User(**user_data)
        return user
    else:
        return None


async def get_all_users() -> List[User]:
    users_data = get_user_collection().find()
    users = [User(**user) for user in users_data]
    return users


async def update_user(user_id: str, updated_data: dict) -> Optional[User]:
    result = get_user_collection().update_one(
        {"_id": ObjectId(user_id)}, {"$set": updated_data}
    )
    if result.modified_count == 1:
        updated_user = get_user_by_id(user_id)
        return updated_user
    else:
        return None


async def delete_user(user_id: str) -> bool:
    result = get_user_collection().delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1
