from __future__ import annotations

from sqlalchemy import Sequence, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .equipment import Equipment
    from .farmer import Farmer

class Farm(Base):
    __tablename__ = "farms"

    id_seq = Sequence(f'{__tablename__}_id_seq');
    id: Mapped[int] = mapped_column(
            id_seq,
            primary_key=True,
            server_default=id_seq.next_value())
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(150))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    equipments: Mapped["Equipment"] = relationship(back_populates="farm")
    farmers: Mapped["Farmer"] = relationship(back_populates="farm")

    def __repr__(self):
        return (f"Farm: id={self.id}, name={self.name}, "
                f"location_region={self.location_region}, "
                f"capacity={self.capacity}") #, supervisor_id={self.supervisor_id}")
