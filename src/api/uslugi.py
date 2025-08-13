from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.schemas.uslugi import UslugiAdd
from src.api.dependencies import DBDep
from src.services.uslugi import UslugiService

router = APIRouter(prefix="/uslugi", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_uslugi(db: DBDep):
    return await UslugiService(db).get_uslugi()


@router.post("")
async def create_uslugi(db: DBDep, uslugi_data: UslugiAdd = Body()):
    uslugi = await UslugiService(db).create_uslugi(uslugi_data)
    return {"Status": "OK", "data": uslugi}
