from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ts: datetime
    source: str
    url: Optional[str] = None
    title: Optional[str] = None
    duration_sec: int
    category: Optional[str] = None
    subcategory: Optional[str] = None
    productive_score: float = 0.5
