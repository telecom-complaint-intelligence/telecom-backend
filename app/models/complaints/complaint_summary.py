import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ComplaintSummary(Base):
    __tablename__ = "complaint_summaries"

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

    complexity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL, OTHER
    headline = Column(String(255), nullable=True)
    summary = Column(Text, nullable=False)
    solution_snippet = Column(Text, nullable=True)
    summary_structured = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    complaint = relationship("Complaint", back_populates="summary")
