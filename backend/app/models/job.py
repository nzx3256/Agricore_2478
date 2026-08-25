from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import FieldJobPriority, FieldJobStatus

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
    priority: Mapped["FieldJobPriority"] = mapped_column(SqlEnum(
            FieldJobPriority,
            name="field_job_priority",
            values_callable = lambda enum_cls: [member.value for member in enum_cls]))
    status: Mapped["FieldJobStatus"] = mapped_column(SqlEnum(
            FieldJobStatus,
            name="field_job_status",
            values_callable = lambda enum_cls: [member.value for member in enum_cls]))
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipments.id"))
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmers.id"))

    equipment: Mapped["Equipment"] = relationship(back_populates="field_jobs")
    farmer: Mapped["Farmer"] = relationship(back_populates="field_jobs")
    reports: Mapped["ServiceReport"] = relationship(back_populates="field_job")

    
    def __repr__(self):
        return (f"Field Job: id={self.id}, title={self.title}, "
                f"priority={self.priority}, status={self.status},"
                f"equipment_id={self.equipment_id}, farmer_id={self.farmer_id}")
