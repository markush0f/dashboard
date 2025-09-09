import json
from typing import Dict, Any
from app.infra.ai.openai_client import get_openai
from .constants import STRUCTURED_SCHEMA, PROMPT

from app.core.config import get_settings

MODEL = get_settings().OPENAI_MODEL


def analyze_with_openai(summary: Dict[str, Any]) -> Dict[str, Any]:
    client = get_openai()
    resp = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": PROMPT},
                    {"type": "input_json", "input_json": {"summary": summary}},
                ],
            }
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
    ) # type: ignore[call-arg]

    # Formas seguras de extraer el texto (según SDK 1.40+):
    # 1) Directo:
    if hasattr(resp, "output_text") and resp.output_text:
        return json.loads(resp.output_text)

    # 2) Fallback por contenido (por si cambia el SDK):
    content = resp.output[0].content[0].text  # type: ignore[attr-defined]
    return json.loads(content)
