from fastapi import APIRouter
from starlette import status

from services.generator import random_ideas, random_fruits_veggies, random_animals


router = APIRouter()


@router.get("/ideas", status_code=status.HTTP_200_OK)
async def get_random_ideas():
    return random_ideas()


@router.get("/fruitsAndVeggies", status_code=status.HTTP_200_OK)
async def get_random_fruits_veggies():
    return random_fruits_veggies()


@router.get("/animals", status_code=status.HTTP_200_OK)
async def get_random_animals():
    return random_animals()


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to weird ideas generator"}