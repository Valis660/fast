from src.repositories.base import BaseRepository
from src.models.uslugi import UslugiOrm
from src.schemas.uslugi import Uslugi


class UslugiRepository(BaseRepository):
    model = UslugiOrm
    schema = Uslugi
