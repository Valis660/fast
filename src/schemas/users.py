from pydantic import BaseModel, EmailStr, ConfigDict


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    name: str | None = None


class User(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None


class UserWithHashedPassword(User):
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
