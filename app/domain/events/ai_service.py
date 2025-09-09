from typing import List, Dict, Any
from app.domain.events.schemas import EventIn
from .analytics import summarizer as _summarize
from .analytics import analyzer as _analyze

def summarize(events: List[EventIn]) -> Dict[str, Any]:
    return _summarize.summarize(events)

def analyze_with_openai(summary: Dict[str, Any]) -> Dict[str, Any]:
    return _analyze.analyze_with_openai(summary)
