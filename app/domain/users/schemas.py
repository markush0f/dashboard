from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel

class UsersBase(SQLModel):
    pass  # añade campos compartidos aquí

class UsersCreate(UsersBase):
    pass  # campos requeridos para crear

class UsersRead(UsersBase):
    id: int

class UsersPage(SQLModel):
    total: int
    items: List[UsersRead]
