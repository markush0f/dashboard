from sqlmodel import Session
from .models import Events
from .repository import EventsRepository

class EventsService:
    def __init__(self, session: Session):
        self.repo = EventsRepository(session)

    def list_all(self):
        return self.repo.list_all()

    def create(self, data: dict):
        return self.repo.create(Events(**data))
