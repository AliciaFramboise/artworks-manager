from datetime import timedelta
from typing import Annotated

from decouple import config
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from api.model.user_dto import UserRequest, Token
from database.database import get_db
from services.authService import save_user, authenticate_user, create_access_token
from services.exceptions import InvalidParameterException, AuthenticationFailedException

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]


TOKEN_ACCESS_TIME = config('ACCESS_TOKEN_TIME', default=20)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      user_request: UserRequest):
    user = await save_user(db, user_request)

    return user


@router.post("/token", response_model=Token)
async def login_with_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
        token = await create_access_token(user.username, user.id, user.role, timedelta(minutes=TOKEN_ACCESS_TIME))
        return {'access_token': token, 'token_type': 'bearer'}
    except (InvalidParameterException, AuthenticationFailedException) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate user: {str(e)}")

