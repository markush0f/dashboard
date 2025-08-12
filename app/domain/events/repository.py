from sqlmodel import Session, select
from .models import Events

class EventsRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self):
        return self.session.exec(select(Events)).all()

    def create(self, obj: Events):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
