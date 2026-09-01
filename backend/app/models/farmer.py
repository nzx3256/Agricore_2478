from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .farm import Farm
    from .job import FieldJob

class Farmer(Base):
    __tablename__ = "farmers"

    id_seq = Sequence(f'{__tablename__}_id_seq');
    id: Mapped[int] = mapped_column(
            id_seq,
            primary_key=True,
            server_default=id_seq.next_value())
    full_name: Mapped[str] = mapped_column(String(150))
    farm_id: Mapped[int] = mapped_column(Integer, ForeignKey("farms.id"))

    farm: Mapped["Farm"] = relationship(back_populates="farmers")
    field_jobs: Mapped[list["FieldJob"]] = relationship(back_populates="farmer")

    def __repr__(self) -> str:
        return (f"Farmer: id={self.id}, name={self.full_name}, "
                f"farm_id={self.farm_id}")
