from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    username: str


class User(UserBase):
    id: int
    createdate: datetime
    updatedate: datetime
    bio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True
