from httpx import delete

from src.repositories.base import BaseRepository
from src.models.uslugi import UslugiOrm, RoomsUslugiOrm
from src.repositories.mappers.mappers import UslugiDataMapper
from src.schemas.uslugi import RoomUslugi
from sqlalchemy import select, insert


class UslugiRepository(BaseRepository):
    model = UslugiOrm
    mapper = UslugiDataMapper


class RoomsUslugiRepository(BaseRepository):
    model = RoomsUslugiOrm
    schema = RoomUslugi

    async def set_room_uslugi(self, room_id: int, uslugi_ids: list[int]) -> None:
        get_current_usliugi_ids_query = select(self.model.uslugi_id).filter_by(room_id=room_id)

        res = await self.session.execute(get_current_usliugi_ids_query)
        current_uslugi_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_uslugi_ids) - set(uslugi_ids))
        ids_to_insert: list[int] = list(set(uslugi_ids) - set(current_uslugi_ids))

        if ids_to_delete:
            delete_m2m_uslugi_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.uslugi_id.in_(ids_to_delete),
            )
            await self.session.execute(delete_m2m_uslugi_stmt)
        if ids_to_insert:
            insert_m2m_uslugi_stmt = insert(self.model).values(
                [{"room_id": room_id, "uslugi_id": u_id} for u_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_uslugi_stmt)
