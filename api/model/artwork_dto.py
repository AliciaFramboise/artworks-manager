from pydantic import BaseModel, Field


class ArtworkRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=2000)

    class Config:
        json_schema_extra = {
            'example': {
                "title": "An amazing piece of work Waouh",
                "description": "A bullshit description of an art",
            }
        }
