from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    summary: dict = Field(sa_column_kwargs={"type_": "JSON"})
    analysis: dict = Field(sa_column_kwargs={"type_": "JSON"})
