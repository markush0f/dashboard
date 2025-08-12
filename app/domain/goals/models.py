from typing import Optional
from sqlmodel import SQLModel, Field

class Goals(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Añade aquí tus campos
