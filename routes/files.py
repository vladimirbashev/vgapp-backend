from collections import namedtuple
from typing import Annotated
from fastapi import Depends, APIRouter, File, UploadFile
from auth.deps import get_current_user
from crud import files as crud
from schemas import files as schemas
from sqlalchemy.orm import Session
from config import get_db
from schemas.users import User

router = APIRouter()


@router.get("/files/", response_model=schemas.Files)
def read_files(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, skip=skip, limit=limit)
    count = crud.get_files_count(db)

    FilesResponse = namedtuple('FilesResponse', ['items', 'count'])
    return FilesResponse(files, count)


@router.get("/users/me/files/", response_model=schemas.Files)
def read_files_by_user(current_user: Annotated[User, Depends(get_current_user)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, user_id=current_user.id, skip=skip, limit=limit)
    count = crud.get_files_count(db, user_id=current_user.id)

    FilesResponse = namedtuple('FilesResponse', ['items', 'count'])
    return FilesResponse(files, count)


@router.get("/users/{user_id}/files/", response_model=schemas.Files)
def read_files_by_user(current_user: Annotated[User, Depends(get_current_user)], user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, user_id=user_id, skip=skip, limit=limit)
    count = crud.get_files_count(db, user_id=user_id)

    FilesResponse = namedtuple('FilesResponse', ['items', 'count'])
    return FilesResponse(files, count)


@router.post("/files/", response_model=schemas.File)
def create_file_for_user(current_user: Annotated[User, Depends(get_current_user)], file: UploadFile, db: Session = Depends(get_db)):

    return crud.create_user_file(db=db, user_id=current_user.id, path=file.filename)


@router.delete("/files/{file_id}/", response_model=schemas.FileDelete)
def create_file_for_user(current_user: Annotated[User, Depends(get_current_user)], file_id: int, db: Session = Depends(get_db)):
    return crud.delete_file(db=db, file_id=file_id)
