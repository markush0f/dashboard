from sqlmodel import SQLModel, create_engine
from .settings import settings  

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

def init_db():
    SQLModel.metadata.create_all(engine)
