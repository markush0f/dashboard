from __future__ import annotations
from functools import lru_cache
from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[2]  
CANDIDATE = PROJECT_ROOT / ".env"

env_path = (
    CANDIDATE if CANDIDATE.exists()
    else Path(find_dotenv(filename=".env", raise_error_if_not_found=False))
)
if env_path and env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

model_env_file = str(env_path) if env_path and env_path.exists() else None

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=model_env_file,          
        env_file_encoding="utf-8",
        extra="ignore",
    )
    DATABASE_URL: str
    OPENAI_API_KEY: Optional[str] = None

@lru_cache
def get_settings() -> Settings:
    return Settings()
