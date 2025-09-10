from datetime import datetime, timedelta
from sqlmodel import Session
from app.core.db import engine
from app.domain.events.models import Event

def seed_events():
    base_time = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)

    categories = [
        ("work", "documentation", "https://docs.python.org/3/", "Python docs"),
        ("work", "code", "https://github.com/sqlalchemy/sqlalchemy", "SQLAlchemy repo"),
        ("work", "communication", "https://mail.google.com", "Gmail"),
        ("social", "chat", "https://web.whatsapp.com", "WhatsApp Web"),
        ("social", "video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "YouTube Video"),
        ("news", "tech", "https://techcrunch.com", "TechCrunch"),
        ("news", "general", "https://www.bbc.com/news", "BBC News"),
        ("entertainment", "streaming", "https://www.netflix.com", "Netflix"),
        ("entertainment", "music", "https://open.spotify.com", "Spotify"),
        ("shopping", "electronics", "https://www.amazon.com", "Amazon"),
    ]

    events: list[Event] = []
    current_time = base_time

    for i in range(30):
        cat, subcat, url, title = categories[i % len(categories)]
        duration = (i % 5 + 1) * 60 
        productive = 1.0 if cat == "work" else 0.2 if cat == "social" else 0.0

        events.append(
            Event(
                user_id=1,
                ts=current_time,
                source="browser",
                url=url,
                title=title,
                duration_sec=duration,
                category=cat,
                subcategory=subcat,
                productive_score=productive,
            )
        )

        current_time += timedelta(minutes=10)  

    with Session(engine) as session:
        session.add_all(events)
        session.commit()
        print(f"✅ Insertados {len(events)} eventos de prueba para user_id=1")


if __name__ == "__main__":
    seed_events()
