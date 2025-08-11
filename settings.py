from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str
    OPENAI_API_KEY: Optional[str] = None

settings = Settings()  # pyright: ignore[reportCallIssue]  # Cambio: silenciar falso positivo
