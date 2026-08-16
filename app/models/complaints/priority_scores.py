import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ComplaintPriorityScores(Base):
    __tablename__ = "complaint_priority_scores"

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

    complexity = Column(
        String(50), nullable=False
    )  # LOW, MEDIUM, HIGH, CRITICAL
    complexity_score = Column(Integer, nullable=False)
    weighted_complexity_score = Column(Float, nullable=False)
    weighted_negativity_score = Column(Float, nullable=False)
    total_complexity_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship("Complaint", back_populates="priority_scores")
