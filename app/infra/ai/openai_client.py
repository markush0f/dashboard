from __future__ import annotations
from typing import Optional
from openai import OpenAI, AsyncOpenAI
from app.core.config import get_settings

_client: Optional[OpenAI] = None
_async_client: Optional[AsyncOpenAI] = None

def get_openai() -> OpenAI:
    global _client
    if _client is None:
        api_key = get_settings().OPENAI_API_KEY
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY no está definido en .env")
        _client = OpenAI(api_key=api_key)
    return _client

def get_openai_async() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        api_key = get_settings().OPENAI_API_KEY
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY no está definido en .env")
        _async_client = AsyncOpenAI(api_key=api_key)
    return _async_client
