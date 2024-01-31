import os

from sqlalchemy.orm import Session

from database.model.Artwork import Artwork


async def get_all_artworks(db: Session):
    return db.query(Artwork).all()


async def save_artwork(db: Session, title: str, description: str, filename: str):
    artwork_data = {"title": title, "description": description, "filename": filename}
    db_file = Artwork(**artwork_data)

    db.add(db_file)
    # commit any changes in the session to the real db
    db.commit()
    # get last state of db_file from the db
    db.refresh(db_file)

    return db_file


async def get_artwork_by_id(db: Session, artwork_id: int):
    return db.query(Artwork).filter(Artwork.id == artwork_id).first()


async def update_artwork_by_id(db: Session, artwork_id: int, title: str, description: str):
    artwork_to_update = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if artwork_to_update is None:
        return False

    artwork_to_update.title = title
    artwork_to_update.description = description

    db.add(artwork_to_update)
    db.commit()
    db.refresh(artwork_to_update)

    return artwork_to_update


async def delete_artwork_id(db: Session, artwork_id: int):
    artwork_to_delete = await get_artwork_by_id(db, artwork_id)
    if artwork_to_delete is None:
        return False
    db.query(Artwork).filter(Artwork.id == artwork_id).delete()
    db.commit()

    file_path = os.path.join("uploads", artwork_to_delete.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return artwork_to_delete is not None
