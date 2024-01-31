from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_NAME = config('DATABASE_NAME', default='portfolioapp.db')
DB_URL = config('DATABASE_URL', default='sqlite:///./')
SQLALCHEMY_DATABASE_URL = f"{DB_URL}{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
