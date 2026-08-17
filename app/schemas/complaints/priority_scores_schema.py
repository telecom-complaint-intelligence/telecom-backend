from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PriorityScoresResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    complaint_id: str
    complexity: str
    complexity_score: int
    weighted_complexity_score: float
    weighted_negativity_score: float
    total_complexity_score: float
    created_at: datetime | None = None
