from sqlmodel import Session, select
from .models import Analysis
from .schemas import AnalysisOut
from typing import Dict, Any, List

class AnalysisService:
    def __init__(self, session: Session):
        self.session = session

    def save_analysis(self, user_id: int, summary: Dict[str, Any], analysis: Dict[str, Any]) -> Analysis:
        db_obj = Analysis(user_id=user_id, summary=summary, analysis=analysis)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def list_by_user(self, user_id: int) -> List[AnalysisOut]:
        analyses = self.session.exec(select(Analysis).where(Analysis.user_id == user_id)).all()
        return [AnalysisOut.model_validate(analysis) for analysis in analyses]
