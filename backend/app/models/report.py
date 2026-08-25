from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .job import FieldJob

class ServiceReport(Base):
    __tablename__ = "service_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_url: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    field_job_id: Mapped[int] = mapped_column(Integer, ForeignKey("field_jobs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    field_job: Mapped["FieldJob"] = relationship(back_populates="reports")

    def __repr__(self):
        return (f"ServiceReport: id={self.id}, field_job_id={self.field_job_id}, "
                f"file_url={self.file_url}")
