from datetime import datetime
from typing import Iterable, List, Optional
from sqlmodel import Session, select
from sqlalchemy import func, select as sa_select
from .models import Event
from typing import Any, Sequence, cast
from sqlalchemy import desc

class EventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, ev: Event) -> Event:
        self.session.add(ev)
        self.session.commit()
        self.session.refresh(ev)
        return ev

    def add_many(self, events: Iterable[Event]) -> int:
        self.session.add_all(list(events))
        self.session.commit()
        # no refrescamos ids por rendimiento (no los devolvemos en /batch)
        return len(list(events))

    
    def list(self, offset: int = 0, limit: int = 50) -> Sequence[Event]:
        stmt = (
            select(Event)
            .order_by(desc(cast(Any, Event.ts)))  
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(stmt).all()

    def count(self) -> int:
        stmt = select(func.count()).select_from(Event)
        total = self.session.exec(stmt).one()   
        return int(total)

    def list_for_analysis(
        self,
        user_id: Optional[int] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[Event]:
        stmt = select(Event)
        if user_id is not None:
            stmt = stmt.where(Event.user_id == user_id)
        if start:
            stmt = stmt.where(Event.ts >= start)
        if end:
            stmt = stmt.where(Event.ts <= end)
        return list(self.session.exec(stmt))