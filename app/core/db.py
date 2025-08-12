# app/core/db.py
from sqlmodel import create_engine
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

def init_db():
    pass  # Cambio: no crear tablas automáticamente
