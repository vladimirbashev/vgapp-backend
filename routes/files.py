from collections import namedtuple
from typing import Optional

from fastapi import Depends, APIRouter
from crud import files as crud
from schemas import files as schemas
from sqlalchemy.orm import Session

from config import get_db

router = APIRouter()

@router.get("/files/", response_model=schemas.Files)
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, skip=skip, limit=limit)
    count = crud.get_files_count(db)

    FilesResponse = namedtuple('FilesResponse', ['items', 'count'])
    return FilesResponse(files, count)


@router.get("/users/{user_id}/files/", response_model=schemas.Files)
def read_articles(user_id: Optional[int], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, user_id=user_id, skip=skip, limit=limit)
    count = crud.get_files_count(db, user_id=user_id)

    FilesResponse = namedtuple('FilesResponse', ['items', 'count'])
    return FilesResponse(files, count)



@router.post("/users/{user_id}/files/", response_model=schemas.File)
def create_article_for_user(
    user_id: int, file: schemas.FileCreate, db: Session = Depends(get_db)
):
    return crud.create_user_file(db=db, file=file, user_id=user_id)
