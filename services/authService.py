from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.model.user_dto import UserRequest
from database.model.Users import Users


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


async def authenticate_user(db: Session, bcrypt: CryptContext, username: str, password:str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    return bcrypt.verify(password, user.hashed_password)
