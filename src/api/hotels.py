from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, DBDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}",
            summary="Получение данных отеля",
            description="Тут можно получить данные одного отеля по ID",)
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("",
         summary="Получение данных отелей",
         description="Тут можно получить информацию обо всех отелях",)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.post("",
          summary="Добавление отеля",
          description="Тут можно добавить новый отель",)
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 2",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель У фонтана",
                    "location": "Дубай, ул. Шейха, 1",
                }
            }
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


@router.put("/{hotel_id}",
         summary="Редактирование информации об отеле",
        description="Тут можно отредактировать информацию об отеле",)
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}



@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Обновление данных об отеле: name или title")
async def partially_edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удаление отеля",
            description="Тут можно удалить отель",)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"Status": "OK"}