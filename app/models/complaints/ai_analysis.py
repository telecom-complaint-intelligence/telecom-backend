import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ComplaintAIAnalysis(Base):
    __tablename__ = "complaint_ai_analysis"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    complaint_id = Column(
        String(36),
        ForeignKey("complaints.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    category_confidence = Column(Float, nullable=True)
    negativity_score = Column(Float, nullable=True)
    sentiment_score = Column(Float, nullable=True)

    # Technical Information (Hybrid Extraction)
    component = Column(JSON, nullable=True)
    failure_type = Column(JSON, nullable=True)
    scope = Column(String(50), nullable=True)
    service_impact = Column(String(50), nullable=True)
    duration_hours = Column(Float, nullable=True)
    occurrence_pattern = Column(String(50), nullable=True)

    # Solution Agent & High Agent outputs
    solution_a = Column(
        Text, nullable=True
    )  # Initial/Customer-facing solution instructions
    solution_high = Column(
        Text, nullable=True
    )  # High/Critical technical dispatch / engineering action plan
    warnings = Column(
        JSON, nullable=True
    )  # Safety warnings for non-destructive actions
    evidence = Column(JSON, nullable=True)  # Linked Knowledge Base evidence
    confidence_score = Column(Float, nullable=True)  # Overall agent confidence

    # High-Council Multi-Agent Reasoning & Escalation fields
    diagnosis = Column(String(255), nullable=True)
    root_cause = Column(Text, nullable=True)
    risk_level = Column(String(50), nullable=True)
    policy_status = Column(String(50), nullable=True)
    final_decision = Column(String(100), nullable=True)
    critic_feedback = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=True)

    extraction_source = Column(String(50), nullable=True)
    lowest_confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship("Complaint", back_populates="ai_analysis")
