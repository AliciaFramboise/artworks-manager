from pydantic import BaseModel


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
