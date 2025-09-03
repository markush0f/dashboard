from typing import List, Dict, Any
from urllib.parse import urlparse
from app.domain.events.schemas import EventIn

def _domain_of(url: str) -> str:
    try:
        host = urlparse(url).hostname or ""
        return host.replace("www.", "") if host else "invalid"
    except Exception:
        return "invalid"

def summarize(events: List[EventIn]) -> Dict[str, Any]:
    rows = [e for e in events if e.duration_sec >= 3 and _domain_of(e.url) != "invalid"]
    rows.sort(key=lambda e: e.ts)

    by_day: Dict[str, int] = {}
    by_cat: Dict[str, int] = {}
    by_dom: Dict[str, int] = {}
    total = 0
    prod_w = 0.0

    for e in rows:
        day = e.ts.date().isoformat()
        dom = _domain_of(e.url)
        by_day[day] = by_day.get(day, 0) + e.duration_sec
        cat = e.category or "uncategorized"
        by_cat[cat] = by_cat.get(cat, 0) + e.duration_sec
        by_dom[dom] = by_dom.get(dom, 0) + e.duration_sec
        total += e.duration_sec
        prod_w += e.duration_sec * (e.productive_score or 0.0)

    series = [{"date": d, "seconds": s} for d, s in sorted(by_day.items())]
    categories = [{"category": c, "seconds": s} for c, s in sorted(by_cat.items(), key=lambda x: -x[1])]
    top_domains = [{"domain": d, "seconds": s} for d, s in sorted(by_dom.items(), key=lambda x: -x[1])[:10]]
    productivity = round(prod_w / total, 2) if total else 0.0

    return {
        "window": {
            "start": series[0]["date"] if series else None,
            "end": series[-1]["date"] if series else None,
            "days": len(series),
        },
        "totals": {
            "seconds": total,
            "hours": round(total / 3600, 2),
            "productivity": productivity,
        },
        "series": series,
        "categories": categories,
        "topDomains": top_domains,
    }
