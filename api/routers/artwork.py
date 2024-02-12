import os
from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, UploadFile, Form, File, Depends
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from services.artworkService import get_all_artworks, save_artwork, update_artwork_by_id, delete_artwork_id, \
    get_artwork_by_id
from services.authService import get_current_user
from services.exceptions import InvalidParameterException

router = APIRouter(
    prefix='/artwork',
    tags=['artwork']
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency):
    return await get_all_artworks(db)


@router.get("/{artwork_id}", status_code=status.HTTP_200_OK)
async def get_artwork(user: user_dependency,
                      db: db_dependency,
                      artwork_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    artwork = await get_artwork_by_id(db, artwork_id)
    if artwork is not None:
        return artwork
    raise HTTPException(status_code=404, detail='Artwork not found.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artwork(user: user_dependency,
                         db: db_dependency,
                         title: str = Form(...),
                         description: str = Form(...),
                         file: UploadFile = File(...)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    try:
        # Save file to server
        with open(f"uploads/{file.filename}", "wb") as f:
            f.write(file.file.read())

        # Create file record in the database
        db_file = await save_artwork(db, title, description, file.filename)

        return {"file_id": db_file.id, "title": title, "description": description, "filename": file.filename}
    except Exception as e:
        # Handle exceptions (e.g., file upload failure)
        raise HTTPException(status_code=500, detail=f"Failed to upload artwork: {str(e)}")


@router.put("/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_artwork(user: user_dependency,
                         db: db_dependency,
                         title: str = Form(...),
                         description: str = Form(...),
                         artwork_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    try:
        result = await update_artwork_by_id(db, artwork_id, title, description)
        if not result:
            raise HTTPException(status_code=404, detail='Artwork not found.')

        return {"file_id": result.id, "title": title, "description": description}
    except (Exception, InvalidParameterException) as e:
        # Handle exceptions (e.g., file upload failure)
        raise HTTPException(status_code=500, detail=f"Failed to update artwork: {str(e)}")


@router.delete("/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artwork(user: user_dependency,
                         db: db_dependency,
                         artwork_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    try:
        result = await delete_artwork_id(db, artwork_id)
        return result
    except InvalidParameterException as e:
        raise HTTPException(status_code=404, detail=f"Artwork not found: {str(e)}")
