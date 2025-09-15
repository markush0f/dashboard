from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict

class AnalysisOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    summary: Dict[str, Any]
    analysis: Dict[str, Any]

    model_config = {
        "from_attributes": True
    }