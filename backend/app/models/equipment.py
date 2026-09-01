from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, Sequence, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import EquipmentStatus

from .base import Base

if TYPE_CHECKING:
    from .job import FieldJob
    from .farm import Farm

class Equipment(Base):
    __tablename__ = "equipments"
    __table_args__ = (
        CheckConstraint("fuel_level BETWEEN 0 AND 100", 
                        name = "fuel_level_range"),
    )

    id_seq = Sequence(f'{__tablename__}_id_seq');
    id: Mapped[int] = mapped_column(
            id_seq,
            primary_key=True,
            server_default=id_seq.next_value())
    serial_number: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[EquipmentStatus] = mapped_column(SqlEnum(
            EquipmentStatus,
            name="equipment_status",
            values_callable = lambda enum_cls: [member.value for member in enum_cls]))
    fuel_level: Mapped[float] = mapped_column(Numeric(5,2))
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id"))

    farm: Mapped["Farm"] = relationship(back_populates="equipments")
    field_jobs: Mapped["FieldJob"] = relationship(back_populates="equipment")

    def __repr__(self):
        return (f"Equipment: id={self.id}, serial_number={self.serial_number}, "
                f"model={self.model}, fuel_level={self.fuel_level}, "
                f"farm_id={self.farm_id}")
