from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException, \
    HotelNotFoundException, RoomNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch, Room
from src.schemas.uslugi import RoomUslugiAdd
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filterted_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
        return room

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_uslugi_data = [
            RoomUslugiAdd(room_id=room.id, uslugi_id=u_id) for u_id in room_data.uslugi_ids
        ]
        await self.db.rooms_uslugi.add_bulk(rooms_uslugi_data)
        await self.db.commit()

    async def edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room(room_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_uslugi.set_room_uslugi(room_id, uslugi_ids=room_data.uslugi_ids)
        await self.db.commit()


    async def partially_edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "uslugi_ids" in _room_data_dict:
            await self.db.rooms_uslugi.set_room_uslugi(room_id, uslugi_ids=_room_data_dict["uslugi_ids"])
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException