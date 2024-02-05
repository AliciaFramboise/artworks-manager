from datetime import datetime, timedelta
from typing import Annotated

from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.model.user_dto import UserRequest
from database.model.Users import Users

TOKEN_KEY = config('SECRET_KEY')
ALGORITHM = config('TOKEN_ALGO', default='HS256')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


async def save_user(db: Session, bcrypt: CryptContext, user_request: UserRequest):
    user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt.hash(user_request.password)
    )

    db.add(user_model)
    db.commit()
    return user_model


async def authenticate_user(db: Session, bcrypt: CryptContext, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    return user


async def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, TOKEN_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, TOKEN_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            return False
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        return False
