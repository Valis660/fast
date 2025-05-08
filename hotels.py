from fastapi import Query, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]
@router.get("",
         summary="Получение данных отелей",
         description="Тут можно получить информацию обо всех отелях",)
def get_hotels(id: int | None = Query(None, description="Айдишник"),
               title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_



@router.delete("/{hotel_id}",
            summary="Удаление отеля",
            description="Тут можно удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}

@router.post("",
          summary="Добавление отеля",
          description="Тут можно добавить новый отель",)
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"Status": "OK"}


@router.put("/{hotel_id}",
         summary="Редактирование информации об отеле",
        description="Тут можно отредактировать информацию об отеле",)
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"Status": "OK"}



@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Обновление данных об отеле: name или title")
def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"Status": "OK"}