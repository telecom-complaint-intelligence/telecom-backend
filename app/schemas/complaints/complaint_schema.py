from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.schemas.complaints.address_schema import (
    ComplaintAddressResponse,
)
from app.schemas.complaints.ai_analysis_schema import AIAnalysisResponse
from app.schemas.complaints.priority_scores_schema import PriorityScoresResponse


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ticket_number: str | None = Field(
        None,
        description="Optional ticket number (auto-generated if omitted)",
    )
    complaint: str = Field(
        ...,
        min_length=5,
        description="Customer complaint text",
        validation_alias=AliasChoices("complaint", "complaint1"),
    )

    filling_on_behalf_of: bool = Field(
        default=False,
        description="False = Filing for self (address pulled from profile). True = Filing on behalf of someone else (fill address fields below).",
    )

    # Address fields (only needed when filling_on_behalf_of=True)
    address: str | None = Field(
        None, description="Custom address (required only if on behalf of)"
    )
    city: str | None = Field(
        None, description="Custom city (required only if on behalf of)"
    )
    state: str | None = Field(
        None, description="Custom state (required only if on behalf of)"
    )
    country: str | None = Field("India", description="Custom country (default: India)")
    zipcode: str | None = Field(
        None, description="Custom zipcode (required only if on behalf of)"
    )


class ComplaintUpdate(BaseModel):
    complaint2: str | None = Field(
        None, description="Follow-up customer complaint or clarification"
    )
    response: str | None = Field(None, description="Updated AI/Agent triage response")
    customer_feedback: bool | None = Field(
        None,
        description="True = solution worked, False = issue persisted / broken",
    )
    status: str | None = Field(
        None, description="OPEN | IN_PROGRESS | ESCALATED | RESOLVED | CLOSED"
    )
    closing_time_stamp: datetime | None = None


class ComplaintFeedbackRequest(BaseModel):
    customer_feedback: bool = Field(
        ...,
        description="True if suggested solution resolved the issue; False if issue persists",
    )


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ticket_number: str | None = None
    user_id: str | None = None

    # Text fields
    complaint1: str
    response: str | None = None
    complaint2: str | None = None

    # Customer Feedback
    customer_feedback: bool | None = None

    # On Behalf Of flag
    filling_on_behalf_of: bool = False

    status: str
    category: str | None = None

    # Timestamps
    timestamp: datetime | None = None
    created_at: datetime | None = None
    closing_time_stamp: datetime | None = None

    # Address & Intelligence
    complaint_address: ComplaintAddressResponse | None = None
    resolved_address: ComplaintAddressResponse | None = None
    ai_analysis: AIAnalysisResponse | None = None
    priority_scores: PriorityScoresResponse | None = None
