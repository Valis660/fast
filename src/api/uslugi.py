from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.uslugi import UslugiAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task

router = APIRouter(prefix="/uslugi", tags=["Удобства"])

@router.get("")
# @cache(expire=10)
async def get_uslugi(db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.uslugi.get_all()

@router.post("")
async def create_uslugi(db: DBDep, uslugi_data: UslugiAdd = Body()):
    uslugi = await db.uslugi.add(uslugi_data)
    await db.commit()

    #test_tasks.delay()

    return {"Status": "OK", "data": uslugi}

