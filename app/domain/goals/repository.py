from sqlmodel import Session, select
from ..goals.models import Goals

class GoalsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Goals)).all()

    def create(self, obj: Goals):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
