from __future__ import annotations

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .equipment import Equipment

class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(150))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)
    #supervisor_id: Mapped[int] = mapped_column(Integer, ForeignKey("supervisor.id"))
    #supervisor: Mapped["Supervisor"] = relationship(back_populates="supervisor")

    equipment: Mapped["Equipment"] = relationship(back_populates="farm")

    def __repr__(self):
        return (f"Farm: id={self.id}, name={self.name}, "
                f"location_region={self.location_region}, "
                f"capacity={self.capacity}, supervisor_id={self.supervisor_id}")
