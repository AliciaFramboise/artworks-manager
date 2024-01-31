import os
from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, UploadFile, Form, File, Depends
from sqlalchemy.orm import Session
from starlette import status

from database.database import get_db
from services.artworkService import get_all_artworks, save_artwork, update_artwork_by_id, delete_artwork_id, \
    get_artwork_by_id

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/artwork", status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency):
    return await get_all_artworks(db)


@router.get("/artwork/{artwork_id}", status_code=status.HTTP_200_OK)
async def get_artwork(db: db_dependency, artwork_id: int = Path(gt=0)):
    artwork = await get_artwork_by_id(db, artwork_id)
    if artwork is not None:
        return artwork
    raise HTTPException(status_code=404, detail='Artwork not found.')


@router.post("/artwork", status_code=status.HTTP_201_CREATED)
async def create_artwork(db: db_dependency,
                         title: str = Form(...),
                         description: str = Form(...),
                         file: UploadFile = File(...)):
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


@router.put("/artwork/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_artwork(db: db_dependency,
                         title: str = Form(...),
                         description: str = Form(...),
                         artwork_id: int = Path(gt=0)):
    try:
        result = await update_artwork_by_id(db, artwork_id, title, description)
        if not result:
            raise HTTPException(status_code=404, detail='Artwork not found.')

        return {"file_id": result.id, "title": title, "description": description}
    except Exception as e:
        # Handle exceptions (e.g., file upload failure)
        raise HTTPException(status_code=500, detail=f"Failed to update artwork: {str(e)}")


@router.delete("/artwork/{artwork_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artwork(db: db_dependency, artwork_id: int = Path(gt=0)):
    result = await delete_artwork_id(db, artwork_id)
    if not result:
        raise HTTPException(status_code=404, detail='Artwork not found.')
