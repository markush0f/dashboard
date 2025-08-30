from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.domain.users.models import User

class Event(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    ts: datetime = Field(default_factory=datetime.utcnow, index=True)
    source: str = Field(default="browser")
    url: Optional[str] = None
    title: Optional[str] = None
    duration_sec: int = Field(default=0)
    category: Optional[str] = None
    subcategory: Optional[str] = None
    productive_score: float = Field(default=0.0)

    user: "User" = Relationship(back_populates="events")


# https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/define-relationships-attributes/#declare-relationship-attributes


# {
#   "email": "markus@example.com",
#   "full_name": "Markus Abramian",
#   "disabled": false
# }
