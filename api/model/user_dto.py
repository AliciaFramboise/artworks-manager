from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str
    role: str

    email: str
    first_name: str
    last_name: str
