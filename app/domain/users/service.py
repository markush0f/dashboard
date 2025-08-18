from typing import Tuple, List
from sqlmodel import Session
from .models import Users
from .repository import UsersRepository
from .schemas import UsersCreate

class UsersService:
    def __init__(self, session: Session):
        self.repo = UsersRepository(session)

    def list_with_total(self, offset: int, limit: int) -> tuple[list[Users], int]:
        items_seq = self.repo.list(offset=offset, limit=limit)
        items: List[Users] = list(items_seq)  # normaliza a list para evitar warnings de tipos
        total = self.repo.count()
        return items, total

    def create(self, data: UsersCreate) -> Users:
        obj = Users.model_validate(data)
        return self.repo.create(obj)
