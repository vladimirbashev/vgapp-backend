from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException

from auth.deps import get_current_user
from crud import users as crud
from schemas import users as schemas
from sqlalchemy.orm import Session

from config import get_db
from schemas.users import User

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# user: SystemUser = Depends(get_current_user)
# current_user: Annotated[User, Depends(get_current_user)]

@router.get("/users/me/", response_model=schemas.User)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


