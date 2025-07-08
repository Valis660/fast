from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep
from src.schemas.uslugi import RoomUslugiAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/")
@cache(expire=10)
async def get_rooms(db: DBDep,
        hotel_id: int,
        date_from: date = Query(examples='2025-07-01'),
        date_to: date = Query(examples='2025-07-10'),):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_uslugi_data = [RoomUslugiAdd(room_id=room.id, uslugi_id=u_id) for u_id in room_data.uslugi_ids]
    await db.rooms_uslugi.add_bulk(rooms_uslugi_data)
    await db.commit()

    return {"Status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_uslugi.set_room_uslugi(room_id, uslugi_ids=room_data.uslugi_ids)
    await db.commit()
    return {"Status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "uslugi_ids" in _room_data_dict:
        await db.rooms_uslugi.set_room_uslugi(room_id, uslugi_ids=_room_data_dict["uslugi_ids"])
    await db.commit()
    return {"Status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"Status": "OK"}