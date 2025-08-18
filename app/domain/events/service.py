from typing import Iterable, List
from sqlmodel import Session
from .models import Event
from .schemas import EventIn

class EventService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: EventIn) -> Event:
        from .repository import EventRepository
        repo = EventRepository(self.session)
        ev = Event.model_validate(data)
        return repo.create(ev)
 
    def create_batch(self, items: Iterable[EventIn]) -> int:
        from .repository import EventRepository
        repo = EventRepository(self.session)
        events = [Event.model_validate(i) for i in items]
        return repo.add_many(events)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[Event], int]:
        from .repository import EventRepository
        repo = EventRepository(self.session)
        items = list(repo.list(offset=offset, limit=limit))  
        total = repo.count()
        return items, total
