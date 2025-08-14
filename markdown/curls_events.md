## Endpoints `/events` - Ejemplos en Markdown

### 1️⃣ Listar eventos

```bash
curl -X GET "http://localhost:8000/events?offset=0&limit=50"
```

### 2️⃣ Crear un evento

```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "ts": "2025-08-14T15:30:00",
    "source": "chrome",
    "url": "https://openai.com",
    "title": "OpenAI",
    "duration_sec": 120,
    "category": "research",
    "subcategory": "ai",
    "productive_score": 0.95
  }'
```

### 3️⃣ Crear varios eventos en batch

```bash
curl -X POST "http://localhost:8000/events/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "ts": "2025-08-14T15:30:00",
        "source": "chrome",
        "url": "https://example.com",
        "title": "Example",
        "duration_sec": 60,
        "category": "news",
        "subcategory": "tech",
        "productive_score": 0.8
      },
      {
        "ts": "2025-08-14T16:00:00",
        "source": "firefox",
        "url": "https://openai.com",
        "title": "OpenAI",
        "duration_sec": 180,
        "category": "research",
        "subcategory": "ai",
        "productive_score": 0.95
      }
    ]
  }'
```

### 4️⃣ Combinado para pruebas rápidas

```bash
# Listar inicial
curl -X GET "http://localhost:8000/events"

# Crear uno
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{"ts":"2025-08-14T15:30:00","source":"chrome","url":"https://openai.com","title":"OpenAI","duration_sec":120,"category":"research","subcategory":"ai","productive_score":0.95}'

# Crear batch
curl -X POST "http://localhost:8000/events/batch" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"ts":"2025-08-14T15:30:00","source":"chrome","url":"https://example.com","title":"Example","duration_sec":60,"category":"news","subcategory":"tech","productive_score":0.8},{"ts":"2025-08-14T16:00:00","source":"firefox","url":"https://openai.com","title":"OpenAI","duration_sec":180,"category":"research","subcategory":"ai","productive_score":0.95}]}'

# Listar final
curl -X GET "http://localhost:8000/events?offset=0&limit=50"
```
