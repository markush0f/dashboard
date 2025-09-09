from asyncio import events
from typing import Dict, Any, Optional, Iterable
from sqlmodel import Session

from app.domain.events import ai_service
from .models import Event
from .schemas import EventIn
from datetime import datetime


class EventService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: EventIn) -> Event:
        from .repository import EventRepository

        repo = EventRepository(self.session)
        ev = Event.model_validate(data.model_dump())
        return repo.create(ev)

    def create_batch(self, items: Iterable[EventIn]) -> int:
        from .repository import EventRepository

        repo = EventRepository(self.session)
        events = [Event.model_validate(i.model_dump()) for i in items]
        return repo.add_many(events)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[Event], int]:
        from .repository import EventRepository

        repo = EventRepository(self.session)
        items = list(repo.list(offset=offset, limit=limit))
        total = repo.count()
        return items, total

    def analyze_events(
        self,
        user_id: Optional[int] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        from .repository import EventRepository

        repo = EventRepository(self.session)
        
        events = repo.list_for_analysis(user_id=user_id, start=start, end=end)
        if not events:
            return {"detail": "No events to analyze"}

        # ✅ Convertimos Event (ORM) -> EventIn (schema)
        dto_events = [EventIn.model_validate(e) for e in events]

        # Paso 1: resumen
        summary = ai_service.summarize(dto_events)

        # Paso 2: análisis IA
        return ai_service.analyze_with_openai(summary)
