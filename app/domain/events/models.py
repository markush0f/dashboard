from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ts: datetime = Field(index=True)          
    source: str = Field(default="browser")     
    url: Optional[str] = None
    title: Optional[str] = None
    duration_sec: int = 0                      
    category: Optional[str] = None
    subcategory: Optional[str] = None
    productive_score: float = 0.0 
