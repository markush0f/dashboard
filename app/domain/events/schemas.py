from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
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

class AnalysisIn(SQLModel):
    event_id: int
    
    
class AnalyzeRequest(BaseModel):
    events: List[EventIn] = Field(default_factory=list)

class AnalyzeSummary(BaseModel):
    window: Dict[str, Any]
    totals: Dict[str, Any]
    series: List[Dict[str, Any]]
    categories: List[Dict[str, Any]]
    topDomains: List[Dict[str, Any]]

class AnalyzeResponse(BaseModel):
    kpis: Dict[str, Any]
    anomalias: List[Dict[str, Any]] = Field(default_factory=list)
    patrones: List[str] = Field(default_factory=list)
    recomendaciones: List[str] = Field(default_factory=list)
    explicacion_corta: str