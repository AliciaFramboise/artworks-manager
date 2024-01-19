import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import artwork, ideas
from database.database import Base, engine

app = FastAPI()

app.include_router(artwork.router)
app.include_router(ideas.router)

origins = {"http://localhost:3000", "localhost:3000"}

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = os.path.join(os.getcwd(), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
