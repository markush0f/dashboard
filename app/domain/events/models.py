from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import Mapped, relationship

from app.domain.users.models import User

class Event(SQLModel, table=True):
    __tablename__ = "event" #type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    # Si ya tienes datos, déjala Optional y migra en dos pasos antes de poner NOT NULL
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)

    ts: datetime = Field(index=True, default_factory=datetime.utcnow)
    source: str = Field(default="browser")
    url: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    duration_sec: int = Field(default=0)
    category: Optional[str] = Field(default=None)
    subcategory: Optional[str] = Field(default=None)
    productive_score: float = Field(default=0.0)

    user: Mapped[Optional["User"]] = relationship(back_populates="events")
