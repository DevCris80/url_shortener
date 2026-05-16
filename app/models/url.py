from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    long_url: Mapped[str] = mapped_column(String(2048), index=True)
    short_url: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    clicks: Mapped[int] = mapped_column(default=0)
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    user: Mapped[User] = relationship(back_populates="urls")