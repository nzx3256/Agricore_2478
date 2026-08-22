from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models import equipment

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .equipment import Equipment
    from .farmer import Farmer
    from .report import ServiceReport

class FieldJob(Base):
    __tablename__ = "field_jobs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    #priority
    #status = 
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipments.id"))
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmer.id"))

    equipment = Mapped["Equipment"] = relationship(backpopulate="field_jobs")
    farmer = Mapped["Farmer"] = relationship(back_populate="field_jobs")

    
    def __repr__(self):
        return (f"Field Job: id={self.id}, title={self.title}, "
                f"priority={self.priority}, status={self.status},"
                f"equipment_id={self.equipment_id}, farmer_id={self.farmer_id}")
