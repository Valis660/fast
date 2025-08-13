from src.schemas.uslugi import UslugiAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task

class UslugiService(BaseService):
    async def create_uslugi(self, uslugi_data: UslugiAdd):
        uslugi = await self.db.uslugi.add(uslugi_data)
        await self.db.commit()

        test_task.delay()
        return uslugi

    async def get_uslugi(self):
        return await self.db.uslugi.get_all()