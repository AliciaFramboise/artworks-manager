from sqlalchemy import Column, Integer, String

from database.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String)

    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
