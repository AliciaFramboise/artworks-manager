from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from api.model.user_dto import UserRequest
from database.database import get_db
from services.authService import save_user, authenticate_user

bcrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      user_request: UserRequest):
    user = await save_user(db, bcrypt, user_request)

    return user


@router.post("/token")
async def login_with_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    if not await authenticate_user(db, bcrypt, form_data.username, form_data.password):
        return 'Failed Authentication'

    return 'Successfully Authenticate'

