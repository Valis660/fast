from fastapi import FastAPI, Query, Body
import uvicorn
app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]
@app.get("/hotels",
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

@app.delete("/hotels/{hotel_id}",
            summary="Удаление отеля",
            description="Тут можно удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}

@app.post("/hotels",
          summary="Добавление отеля",
          description="Тут можно добавить новый отель",)
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title})
    return {"Status": "OK"}


@app.put("/hotels/{hotel_id}",
         summary="Редактирование информации об отеле",
        description="Тут можно отредактировать информацию об отеле",)
def edit_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"Status": "OK"}



@app.patch("/hotels/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Обновление данных об отеле: name или title")
def partially_edit_hotel(
    hotel_id: int,
    title: str | None  = Body(None),
    name: str | None  = Body(None)
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"Status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)