from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str
    password: str
    role: str

    email: str
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
