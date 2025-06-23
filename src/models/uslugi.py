from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UslugiOrm(Base):
    __tablename__ = "uslugi"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))



class RoomsUslugi(Base):
    __tablename__ = "rooms_uslugi"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    uslugi_id: Mapped[int] = mapped_column(ForeignKey("uslugi.id"))