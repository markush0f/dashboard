import json
from typing import Dict, Any
from app.infra.ai.openai_client import get_openai
from .constants import STRUCTURED_SCHEMA, PROMPT
from app.core.config import get_settings

MODEL = get_settings().OPENAI_MODEL

def analyze_with_openai(summary: Dict[str, Any]) -> Dict[str, Any]:
    client = get_openai()

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Eres analista de datos y devuelves SOLO JSON."},
            {"role": "user", "content": f"{PROMPT}\n\n{json.dumps({'summary': summary}, ensure_ascii=False)}"},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "AnalisisUsoNavegador",
                "schema": STRUCTURED_SCHEMA,
                "strict": True,
            },
        },
        temperature=0.1,
    )

    message = resp.choices[0].message
    content = message.content

    if not content:
        raise ValueError("El modelo no devolvió contenido en la respuesta")

    return json.loads(content)
