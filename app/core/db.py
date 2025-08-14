# app/core/db.py
from typing import Generator
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://markus:1234@localhost:5432/dashboard_db")
engine = create_engine(
    DATABASE_URL,  # type: ignore
    pool_pre_ping=True,
    echo=False,
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
