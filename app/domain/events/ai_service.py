from __future__ import annotations
from typing import Literal
from openai import OpenAI
from app.infra.ai.openai_client import get_openai

Category = Literal["work","dev","research","social","video","news","other"]

SYSTEM = "Eres un clasificador. Devuelve solo un JSON con keys category y subcategory."

PROMPT = """Clasifica este evento de navegación:
title: {title}
url: {url}
Deberías responder solo JSON, p.ej. {{"category":"dev","subcategory":"code-hosting"}}"""

class EventAIService:
    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client or get_openai()

    def classify(self, *, title: str | None, url: str) -> dict:
        msg = PROMPT.format(title=title or "", url=url)
        resp = self.client.chat.completions.create(  # API de chat
            model="gpt-5",  # elige el más conveniente de tu plan
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": msg},
            ],
            temperature=0
        )
        text = resp.choices[0].message.content or "{}"
        # parsea JSON de forma robusta
        import json
        try:
            data = json.loads(text)
        except Exception:
            data = {"category":"other","subcategory":None}
        return data
