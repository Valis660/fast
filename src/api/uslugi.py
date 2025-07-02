import json
from fastapi import APIRouter, Body

from src.init import redis_manager
from src.schemas.uslugi import UslugiAdd
from src.api.dependencies import DBDep
router = APIRouter(prefix="/uslugi", tags=["Удобства"])

@router.get("")
async def get_uslugi(db: DBDep):
    uslugi_from_cache = await redis_manager.get("uslugi")
    print(f"{uslugi_from_cache=}")
    if not uslugi_from_cache:
        print("ИДУ В БАЗУ ДАННЫХ")
        uslugi = await db.uslugi.get_all()
        uslugi_schemas: list[dict] = [f.model_dump() for f in uslugi]
        uslugi_json = json.dumps(uslugi_schemas)
        await redis_manager.set("uslugi", uslugi_json, 10)

        return uslugi
    else:
        uslugi_dict = json.loads(uslugi_from_cache)
        return uslugi_dict

@router.post("")
async def create_uslugi(db: DBDep, uslugi_data: UslugiAdd = Body()):
    uslugi = await db.uslugi.add(uslugi_data)
    await db.commit()
    return {"Status": "OK", "data": uslugi}