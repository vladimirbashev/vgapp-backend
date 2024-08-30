from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.utils import verify_password, create_access_token
from config import get_db
from schemas import token as schemas
from crud import users as crud
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("/token/", response_model=schemas.TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return JSONResponse({"access_token": create_access_token(user.email), "token_type": "bearer"})

