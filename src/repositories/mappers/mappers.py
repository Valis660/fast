from src.models.bookings import BookingsOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.models.uslugi import UslugiOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User
from src.schemas.uslugi import Uslugi


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class UslugiDataMapper(DataMapper):
    db_model = UslugiOrm
    schema = Uslugi