from pydantic import BaseModel, ConfigDict

class UslugiAdd(BaseModel):
    title: str


class Uslugi(UslugiAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

