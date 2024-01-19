from database.database import Base
from sqlalchemy import Column, Integer, String, MetaData, Table

metadata = MetaData()


class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    filename = Column(String)
    # owner_id = Column(Integer, ForeignKey("users.id"))
