import os

from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import artwork, ideas, auth, users
from database.database import Base, engine

app = FastAPI()

app.include_router(artwork.router)
app.include_router(ideas.router)
app.include_router(auth.router)
app.include_router(users.router)


URL = config('APP_URL', default='localhost')
PORT = config('APP_PORT', default='3000')
origins = {f"http://{URL}:{PORT}", f"{URL}:{PORT}"}

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
