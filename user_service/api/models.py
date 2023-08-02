from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class RefreshTokenInput(BaseModel):
    refresh_token: str
