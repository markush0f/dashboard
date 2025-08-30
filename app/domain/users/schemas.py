from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel

# Campos comunes (comparten User y UsersCreate/Read)
class UsersBase(SQLModel):
    email: str
    full_name: str
    disabled: bool = False

# Para crear un usuario (sin id porque lo pone la DB)
class UsersCreate(UsersBase):
    pass

# Para devolver un usuario (incluye id)
class UsersRead(UsersBase):
    id: int

# Para paginación de usuarios
class UsersPage(SQLModel):
    total: int
    items: List[UsersRead]
