from src.repositories.base import BaseRepository
from src.models.uslugi import UslugiOrm, RoomsUslugiOrm
from src.schemas.uslugi import Uslugi, RoomUslugi


class UslugiRepository(BaseRepository):
    model = UslugiOrm
    schema = Uslugi


class RoomsUslugiRepository(BaseRepository):
    model = RoomsUslugiOrm
    schema = RoomUslugi