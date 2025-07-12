from src.schemas.uslugi import UslugiAdd


async def test_create_uslugi(db):
    uslugi_data = UslugiAdd(title="Парилка")
    await db.uslugi.add(uslugi_data)
    await db.commit()
