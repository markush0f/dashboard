from sqlmodel import SQLModel, create_engine
from app.core import config

engine = create_engine(
    config.settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

def init_db():
    SQLModel.metadata.create_all(engine)
