import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database.database import Base
from database.model.Artwork import Artwork
from database.model.Users import Users
from main import app
from services.userService import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'marcelinetest', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_artwork():
    artwork = Artwork(
        title="La Baleine à lunettes",
        description="Une baleine à lunettes",
        filename="baleine.png",
    )

    db = TestingSessionLocal()
    db.add(artwork)
    db.commit()
    yield artwork
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM artworks;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="baleine_a_lunettes",
        email="baleine.lunettes@gmail.com",
        first_name="Baleine",
        last_name="Lunettes",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
