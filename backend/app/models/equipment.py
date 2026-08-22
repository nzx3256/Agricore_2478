from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from .enums import EquipmentStatus

from .base import Base

if TYPE_CHECKING:
    from .farm import Farm
    from .job import FieldJob

class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = (
        CheckConstraint("fuel_level BETWEEN 0 AND 100", 
                        name = "fuel_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[EquipmentStatus] = mapped_column(SqlEnum(
            EquipmentStatus,
            name="equipment_status",
            values_callable = lambda enum_cls: [member.value for member in enum_cls]))
    fuel_level: Mapped[float] = mapped_column(Numeric(5,2))
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id"))

    farm: Mapped["Farm"] = mapped_column(back_populate="equipments")
    job: Mapped["FieldJob"] = mapped_column(back_populate="equipment")

    def __repr__(self):
        return (f"Equipment: id={self.id}, serial_number={self.serial_number}, "
                f"model={self.model}, fuel_level={self.fuel_level}, "
                f"farm_id={self.farm_id}")
