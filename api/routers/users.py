from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.model.user_dto import UserVerification
from database.database import get_db
from services.authService import get_current_user
from services.exceptions import AuthenticationFailedException
from services.userService import get_user_by_id, change_user_password

router = APIRouter(
    prefix='/user',
    tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return await get_user_by_id(user, db)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    try:
        updated_user = await change_user_password(user, db, user_verification)
        return updated_user
    except AuthenticationFailedException as e:
        raise HTTPException(status_code=401, detail=f"Error on password change: {str(e)}")

