from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Article(BaseModel):
    title: str
    content: str
    author_email: EmailStr
    created_at: Optional[datetime] = None
    is_published: bool = False
