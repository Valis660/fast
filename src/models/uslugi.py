import typing

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class UslugiOrm(Base):
    __tablename__ = "uslugi"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="uslugi",
        secondary="rooms_uslugi",
    )


class RoomsUslugiOrm(Base):
    __tablename__ = "rooms_uslugi"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    uslugi_id: Mapped[int] = mapped_column(ForeignKey("uslugi.id"))
