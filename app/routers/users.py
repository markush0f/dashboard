from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domain.users.service import UsersService
from app.domain.users.schemas import UsersCreate, UsersRead, UsersPage

router = APIRouter(prefix="/users", tags=["users"])

def get_service(session: Session = Depends(get_session)) -> UsersService:
    return UsersService(session)

@router.get("", response_model=UsersPage)
def list_users(offset: int = 0, limit: int = 50, svc: UsersService = Depends(get_service)):
    items, total = svc.list_with_total(offset=offset, limit=limit)
    return UsersPage(total=total, items=items)  # type: ignore

@router.post("", response_model=UsersRead)
def create_users(payload: UsersCreate, svc: UsersService = Depends(get_service)):
    return svc.create(payload)
