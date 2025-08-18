from typing import Sequence
from sqlmodel import Session, select
from sqlalchemy import func
from .models import Users

class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, offset: int = 0, limit: int = 50) -> Sequence[Users]:
        stmt = select(Users).offset(offset).limit(limit)
        return self.session.exec(stmt).all()

    def count(self) -> int:
        stmt = select(func.count()).select_from(Users)
        # tip-friendly con SQLModel
        return int(self.session.exec(stmt).one())

    def create(self, obj: Users) -> Users:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
