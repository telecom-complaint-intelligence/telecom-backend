import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )
    ticket_number = Column(String(50), unique=True, index=True, nullable=True)
    user_id = Column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Initial Complaint, AI/Agent Triage Response, and Follow-up
    complaint1 = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    complaint2 = Column(Text, nullable=True)

    # Customer Feedback on Suggested Solution (True: worked, False: still broken)
    customer_feedback = Column(Boolean, nullable=True)

    # On Behalf Of flag
    filling_on_behalf_of = Column(Boolean, default=False, nullable=False)

    status = Column(String(50), default="OPEN", nullable=False)
    category = Column(String(100), nullable=True)
    resolved_by = Column(String(50), nullable=True)

    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_timestamp = Column(DateTime, nullable=True)
    follow_up_timestamp = Column(DateTime, nullable=True)
    closing_time_stamp = Column(DateTime, nullable=True)

    # 1-to-1 Relationships
    complaint_address = relationship(
        "ComplaintAddress",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )
    ai_analysis = relationship(
        "ComplaintAIAnalysis",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )
    priority_scores = relationship(
        "ComplaintPriorityScores",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )
    summary = relationship(
        "ComplaintSummary",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )

