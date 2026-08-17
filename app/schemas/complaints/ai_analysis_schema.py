from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AIAnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    complaint_id: str
    category_confidence: float | None = None
    negativity_score: float | None = None
    sentiment_score: float | None = None

    component: list[str] | None = None
    failure_type: list[str] | None = None
    scope: str | None = None
    service_impact: str | None = None
    duration_hours: float | None = None
    occurrence_pattern: str | None = None

    solution_a: str | None = None
    solution_high: str | None = None
    warnings: list[str] | None = None
    evidence: list[dict[str, Any]] | None = None
    confidence_score: float | None = None

    diagnosis: str | None = None
    root_cause: str | None = None
    risk_level: str | None = None
    policy_status: str | None = None
    final_decision: str | None = None
    critic_feedback: str | None = None
    reasoning: str | None = None

    extraction_source: str | None = None
    lowest_confidence: float | None = None
    created_at: datetime | None = None
