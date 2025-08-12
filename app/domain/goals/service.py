from sqlmodel import Session
from ..goals.repository import GoalsRepository

class GoalsService:
    def __init__(self, session: Session):
        self.repo = GoalsRepository(session)

    def list_all(self):
        return self.repo.get_all()

    def create(self, data):
        return self.repo.create(data)
