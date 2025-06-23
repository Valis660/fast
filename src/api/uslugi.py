from fastapi import APIRouter, Body

from src.schemas.uslugi import UslugiAdd
from src.api.dependencies import DBDep
router = APIRouter(prefix="/uslugi", tags=["Удобства"])

@router.get("")
async def get_uslugi(db: DBDep):
    return await db.uslugi.get_all()

@router.post("")
async def create_uslugi(db: DBDep, uslugi_data: UslugiAdd = Body()):
    uslugi = await db.uslugi.add(uslugi_data)
    await db.commit()
    return {"Status": "OK", "data": uslugi}