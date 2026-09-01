from __future__ import annotations

from sqlalchemy import Boolean, Sequence, Enum as SqlEnum, String
from sqlalchemy.orm import Mapped, mapped_column
from .enums import UserRole

from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id_seq: Sequence = Sequence(f"{__tablename__}_id_seq")
    id: Mapped[int] = mapped_column(
            id_seq, 
            primary_key=True, 
            server_default=id_seq.next_value())
    username: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SqlEnum(
            UserRole, name="user_role", 
            values_callable=lambda enum_cls: [member.value for member in enum_cls]))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"User: id={self.id}, username={self.username!r}, is_active={self.is_active}"
