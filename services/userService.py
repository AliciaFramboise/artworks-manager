from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.model.user_dto import UserVerification
from database.model.Users import Users
from services.exceptions import AuthenticationFailedException

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_user_by_id(user: dict, db: Session):
    return db.query(Users).filter(Users.id == user.get('id')).first()


async def change_user_password(user: dict, db: Session, user_verification: UserVerification):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise AuthenticationFailedException("Password is incorrect")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
