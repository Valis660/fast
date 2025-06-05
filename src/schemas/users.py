from pydantic import BaseModel


class UserRequestAdd(BaseModel):
    email: str
    password: str


class UserAdd(BaseModel):
    id: int
    hashed_password: str


class User(BaseModel):
    id: int
    email: str