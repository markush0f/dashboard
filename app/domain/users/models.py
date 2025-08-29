from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.events.models import Event


class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    disabled: bool = Field(default=False)

    events: List["Event"] = Relationship(back_populates="user")
