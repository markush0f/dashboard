from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..core.db import engine
from ..domain.events.service import EventsService

router = APIRouter(prefix="/events", tags=["events"])

def get_session():
    with Session(engine) as s:
        yield s

@router.get("")
def list_events(session: Session = Depends(get_session)):
    svc = EventsService(session)
    return svc.list_all()

@router.post("")
def create_events(payload: dict, session: Session = Depends(get_session)):
    svc = EventsService(session)
    return svc.create(payload)
