from typing import List

from pydantic import BaseModel
from schemas.users import User
from datetime import datetime


class FileBase(BaseModel):
    path: str


class FileCreate(FileBase):
    pass


class FileDelete(BaseModel):
    id: int


class File(FileBase):
    id: int
    user: User
    createdate: datetime
    updatedate: datetime

    class Config:
        orm_mode = True


class Files(BaseModel):
    items: List[File]
    count: int

