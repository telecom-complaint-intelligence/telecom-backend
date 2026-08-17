from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ComplaintSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    complaint_id: str
    complexity: str
    headline: str | None = None
    summary: str
    solution_snippet: str | None = None
    summary_structured: dict[str, Any] | None = None
    created_at: datetime
