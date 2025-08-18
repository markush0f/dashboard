from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel

class EventIn(SQLModel):
    user_id: int
    ts: datetime
    url: str
    title: Optional[str] = None
    duration_sec: int
    source: str = "browser"
    category: Optional[str] = None
    subcategory: Optional[str] = None
    productive_score: float = 0.0

class EventOut(EventIn):
    id: int

class EventBatchIn(SQLModel):
    items: List[EventIn]

class EventPage(SQLModel):
    total: int
    items: List[EventOut]
