from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domain.events.service import EventService
from app.domain.events.schemas import EventIn, EventOut, EventBatchIn, EventPage

router = APIRouter(prefix="/events", tags=["events"])

def get_event_service(session: Session = Depends(get_session)) -> EventService:
    return EventService(session)

@router.get("", response_model=EventPage)
def list_events(
    offset: int = 0,
    limit: int = 50,
    svc: EventService = Depends(get_event_service),
):
    items, total = svc.list_with_total(offset=offset, limit=limit)
    # Pydantic/SQLModel hará la conversión Event -> EventOut automáticamente
    return EventPage(total=total, items=items)

@router.post("", response_model=EventOut)
def create_event(payload: EventIn, svc: EventService = Depends(get_event_service)):
    return svc.create(payload)

@router.post("/batch")
def create_events_batch(batch: EventBatchIn, svc: EventService = Depends(get_event_service)):
    inserted = svc.create_batch(batch.items)
    return {"inserted": inserted}
