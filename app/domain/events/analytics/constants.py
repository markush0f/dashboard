STRUCTURED_SCHEMA = {
    "type": "object",
    "properties": {
        "kpis": {
            "type": "object",
            "properties": {
                "total_horas": {"type": "number"},
                "productividad_media": {"type": "number"},
                "dias": {"type": "integer"},
                "foco_top_categorias": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"category": {"type": "string"}, "porcentaje": {"type": "number"}},
                        "required": ["category", "porcentaje"],
                    },
                },
                "top_dominios": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"domain": {"type": "string"}, "pct": {"type": "number"}},
                        "required": ["domain", "pct"],
                    },
                },
            },
            "required": ["total_horas", "productividad_media", "dias", "foco_top_categorias", "top_dominios"],
        },
        "anomalias": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fecha": {"type": "string"},
                    "metrica": {"type": "string"},
                    "valor": {"type": "number"},
                    "z": {"type": "number"},
                    "criterio": {"type": "string"},
                    "comentario": {"type": "string"},
                },
                "required": ["fecha", "metrica", "valor"],
            },
        },
        "patrones": {"type": "array", "items": {"type": "string"}},
        "recomendaciones": {"type": "array", "items": {"type": "string"}},
        "explicacion_corta": {"type": "string"},
    },
    "required": ["kpis", "recomendaciones", "explicacion_corta"],
}

PROMPT = """Analiza el uso del navegador del usuario y devuelve SOLO JSON válido ajustado al schema.
Datos:
- "totals": segundos totales, horas, productividad (0–100) ponderada por tiempo
- "series": {date, seconds} por día
- "categories": {category, seconds}
- "topDomains": {domain, seconds}

Reglas:
- Outliers diarios: usa |z|>2 sobre series.seconds (media y desviación estándar).
- "foco_top_categorias": top 3 en % del total.
- "top_dominios": top 5 en % del total.
- Recomienda 3–5 acciones concretas.
- No incluyas texto fuera del JSON.
"""
