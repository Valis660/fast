from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
@cache(expire=10)
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}
