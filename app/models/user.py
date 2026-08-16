import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    customer_id = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(String, default="customer", nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    cookie_consent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    # Verification OTP fields
    verification_otp = Column(String(6), nullable=True)
    otp_created_at = Column(DateTime, nullable=True)

    # Department relationship
    department_id = Column(
        String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    profile = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    service_details = relationship(
        "ServiceDetails",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    department = relationship("Department", back_populates="users")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)

    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state_val = Column(String, nullable=True)
    country = Column(String, nullable=True)
    zipcode = Column(String, nullable=True)
    is_complete = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="profile")


class ServiceDetails(Base):
    __tablename__ = "service_details"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    account_ref = Column(String, nullable=True)
    bill_cycle = Column(String, nullable=True)
    active_plan = Column(String, nullable=True)
    connection_status = Column(String, nullable=True)
    plan_usage = Column(String, nullable=True)  # "self" | "shop" | "organization"

    user = relationship("User", back_populates="service_details")


class Department(Base):
    __tablename__ = "departments"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    name = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    users = relationship("User", back_populates="department")
    invitations = relationship("ClientInvitation", back_populates="department")


class ClientInvitation(Base):
    __tablename__ = "client_invitations"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    email = Column(String(100), unique=True, index=True, nullable=False)
    department_id = Column(
        String(36),
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
    )
    token = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_activated = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    department = relationship("Department", back_populates="invitations")
