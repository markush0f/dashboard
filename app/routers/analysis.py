from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domain.analysis.service import AnalysisService
from app.domain.analysis.schemas import AnalysisOut
from app.domain.events.schemas import EventIn
from app.domain.events.service import EventService

router = APIRouter(prefix="/analysis", tags=["analysis"])

def get_analysis_service(session: Session = Depends(get_session)) -> AnalysisService:
    return AnalysisService(session)

@router.post("/{user_id}", response_model=AnalysisOut)
def create_analysis(user_id: int,
                    session: Session = Depends(get_session),
                    svc: AnalysisService = Depends(get_analysis_service)):
    event_svc = EventService(session)
    events = event_svc.list_for_user(user_id=user_id)

    from app.domain.events import ai_service
    events_in = [EventIn.model_validate(e) for e in events]
    summary = ai_service.summarize(events_in)
    analysis = ai_service.analyze_with_openai(summary)

    return svc.save_analysis(user_id, summary, analysis)

@router.get("/{user_id}", response_model=list[AnalysisOut])
def list_analyses(user_id: int, svc: AnalysisService = Depends(get_analysis_service)):
    return svc.list_by_user(user_id)
