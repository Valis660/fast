from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache
from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение данных отелей",
    description="Тут можно получить информацию обо всех отелях",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples="2025-06-01"),
    date_to: date = Query(examples="2025-06-30"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )

@router.get(
    "/{hotel_id}",
    summary="Получение данных отеля",
    description="Тут можно получить данные одного отеля по ID",
)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
        return await db.hotels.get_one(id=hotel_id)
    except ObjectAlreadyExistsException:
        raise HotelNotFoundHTTPExceptio


@router.post(
    "",
    summary="Добавление отеля",
    description="Тут можно добавить новый отель",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 2",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель У фонтана",
                    "location": "Дубай, ул. Шейха, 1",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"Status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Редактирование информации об отеле",
    description="Тут можно отредактировать информацию об отеле",
)
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"Status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Обновление данных об отеле: name или title",
)
async def partially_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data)
    return {"Status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут можно удалить отель",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"Status": "OK"}
