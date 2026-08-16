import random
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.redis import get_cached_data, invalidate_cache, set_cached_data
from app.core.security import get_current_user, get_optional_current_user
from app.models.complaints import (
    Complaint,
    ComplaintAddress,
    ComplaintAIAnalysis,
    ComplaintPriorityScores,
)
from app.models.user import User
from app.schemas.complaints import (
    ComplaintAddressResponse,
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)
from app.services.ai_service import AIServiceClient

router = APIRouter(prefix="/complaints", tags=["Complaints"])

COMPLEXITY_MAP = {
    "low": "LOW",
    "med": "MEDIUM",
    "medium": "MEDIUM",
    "high": "HIGH",
    "critical": "CRITICAL",
}


def generate_ticket_number() -> str:
    return f"TICK-{random.randint(100000, 999999)}"


def _build_complaint_response(complaint: Complaint, db: Session) -> ComplaintResponse:
    """Helper to assemble ComplaintResponse and compute resolved_address dynamically."""
    # 1. Determine resolved address based on filling_on_behalf_of
    resolved_addr = None
    if complaint.filling_on_behalf_of and complaint.complaint_address is not None:
        resolved_addr = ComplaintAddressResponse.model_validate(
            complaint.complaint_address
        )
    elif complaint.user_id:
        user = db.query(User).filter(User.id == complaint.user_id).first()
        if user and user.profile:
            resolved_addr = ComplaintAddressResponse(
                address=user.profile.address,
                city=user.profile.city,
                state=user.profile.state_val,
                country=user.profile.country or "India",
                zipcode=user.profile.zipcode,
            )

    return ComplaintResponse(
        id=complaint.id,
        ticket_number=complaint.ticket_number,
        user_id=complaint.user_id,
        complaint1=complaint.complaint1,
        response=complaint.response,
        complaint2=complaint.complaint2,
        filling_on_behalf_of=complaint.filling_on_behalf_of,
        status=complaint.status,
        category=complaint.category,
        timestamp=complaint.timestamp,
        created_at=complaint.created_at,
        closing_time_stamp=complaint.closing_time_stamp,
        complaint_address=ComplaintAddressResponse.model_validate(
            complaint.complaint_address
        )
        if complaint.complaint_address
        else None,
        resolved_address=resolved_addr,
        ai_analysis=complaint.ai_analysis,
        priority_scores=complaint.priority_scores,
    )


def _process_and_save_complaint(
    payload: ComplaintCreate,
    user: User | None,
    db: Session,
) -> ComplaintResponse:
    """Internal helper to call AI microservice and persist normalized complaint records."""
    complaint_text = payload.complaint
    if not complaint_text or len(complaint_text.strip()) < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Complaint text ('complaint') must be at least 5 characters.",
        )

    # 1. Call telecom-ai-service microservice for AI features & priority classification
    ai_features = AIServiceClient.analyze_complaint(complaint_text)

    # 2. Extract user ID
    user_id = user.id if user else None
    ticket_num = payload.ticket_number or generate_ticket_number()

    # Determine initial AI / triage response
    tech_info = ai_features.get("technical_information") or {}
    solution_val = ai_features.get("solution_a") or ai_features.get("solution")
    if not solution_val:
        comp_str = ", ".join(tech_info.get("component") or ["network equipment"])
        fail_str = ", ".join(tech_info.get("failure_type") or ["general issue"])
        solution_val = f"Automated Triage: Inspect {comp_str} for {fail_str} and verify service restoration."

    # 3. Create Table 1: Core Complaint (complaints)
    db_complaint = Complaint(
        ticket_number=ticket_num,
        user_id=user_id,
        complaint1=complaint_text,
        response=solution_val,
        complaint2=None,
        filling_on_behalf_of=payload.filling_on_behalf_of,
        status="OPEN",
        category=ai_features.get("category"),
    )
    db.add(db_complaint)
    db.flush()  # Generates db_complaint.id for foreign keys

    # 4. Handle Table 2: Custom Address (complaint_address) if filling_on_behalf_of is True
    if payload.filling_on_behalf_of:
        db_addr = ComplaintAddress(
            complaint_id=db_complaint.id,
            address=payload.address,
            city=payload.city,
            state=payload.state,
            country=payload.country or "India",
            zipcode=payload.zipcode,
        )
        db.add(db_addr)

    # 5. Create Table 3: AI Analysis (complaint_ai_analysis)
    db_ai_analysis = ComplaintAIAnalysis(
        complaint_id=db_complaint.id,
        category_confidence=ai_features.get("category_confidence"),
        negativity_score=ai_features.get("negativity_score"),
        sentiment_score=ai_features.get("sentiment_score"),
        component=tech_info.get("component"),
        failure_type=tech_info.get("failure_type"),
        scope=tech_info.get("scope"),
        service_impact=tech_info.get("service_impact"),
        duration_hours=tech_info.get("duration_hours"),
        occurrence_pattern=tech_info.get("occurrence_pattern"),
        solution_a=solution_val,
        extraction_source=ai_features.get("extraction_source"),
        lowest_confidence=ai_features.get("lowest_confidence"),
    )
    db.add(db_ai_analysis)

    # 6. Create Table 4: Priority & Scoring Breakdown (complaint_priority_scores)
    db_priority = ComplaintPriorityScores(
        complaint_id=db_complaint.id,
        complexity=ai_features.get("complexity", "LOW"),
        complexity_score=ai_features.get("complexity_score", 0),
        weighted_complexity_score=ai_features.get("weighted_complexity_score", 0.0),
        weighted_negativity_score=ai_features.get("weighted_negativity_score", 0.0),
        total_complexity_score=ai_features.get("total_complexity_score", 0.0),
    )
    db.add(db_priority)

    # Commit transaction
    db.commit()
    db.refresh(db_complaint)

    # Invalidate cache
    if user_id:
        invalidate_cache(f"user:{user_id}:complaints")
    invalidate_cache("complaints:all*")

    response_data = _build_complaint_response(db_complaint, db)
    # Set cache for the individual complaint
    set_cached_data(
        f"complaint:{db_complaint.id}", response_data.model_dump(mode="json")
    )
    return response_data


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    payload: ComplaintCreate,
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """
    General complaint creation endpoint.
    - complaint1: initial complaint text.
    - filling_on_behalf_of: boolean toggle.
      - If True: stores custom address in complaint_address table.
      - If False: resolves address dynamically from logged-in user profile.
    """
    return _process_and_save_complaint(payload, current_user, db)


@router.post(
    "/me", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED
)
def create_my_complaint(
    payload: ComplaintCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Authenticated Customer Complaint creation.
    - Requires Bearer JWT Token.
    - Automatically guarantees user_id is linked to the authenticated customer.
    """
    return _process_and_save_complaint(payload, current_user, db)


@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: str,
    payload: ComplaintUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Update ticket lifecycle:
    - complaint2: follow-up complaint text / clarification.
    - response: updated response or technician note.
    - status: 'OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'.
    - Auto-sets closing_time_stamp when marked RESOLVED or CLOSED.
    """
    complaint = (
        db.query(Complaint)
        .options(
            joinedload(Complaint.complaint_address),
            joinedload(Complaint.ai_analysis),
            joinedload(Complaint.priority_scores),
        )
        .filter(Complaint.id == complaint_id)
        .first()
    )
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ID '{complaint_id}' not found",
        )

    if payload.complaint2 is not None:
        complaint.complaint2 = payload.complaint2
    if payload.response is not None:
        complaint.response = payload.response
    if payload.status is not None:
        complaint.status = payload.status
        if payload.status in ["RESOLVED", "CLOSED"]:
            complaint.closing_time_stamp = payload.closing_time_stamp or datetime.now(
                UTC
            ).replace(tzinfo=None)

    db.commit()
    db.refresh(complaint)

    # Invalidate cache
    invalidate_cache(f"complaint:{complaint_id}")
    if complaint.user_id:
        invalidate_cache(f"user:{complaint.user_id}:complaints")
    invalidate_cache("complaints:all*")

    response_data = _build_complaint_response(complaint, db)
    set_cached_data(f"complaint:{complaint_id}", response_data.model_dump(mode="json"))
    return response_data


@router.get("/me", response_model=list[ComplaintResponse])
def get_my_complaints(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieves only the complaint tickets submitted by the authenticated customer.
    Requires Bearer JWT Authorization header.
    """
    cache_key = f"user:{current_user.id}:complaints"
    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    complaints = (
        db.query(Complaint)
        .options(
            joinedload(Complaint.complaint_address),
            joinedload(Complaint.ai_analysis),
            joinedload(Complaint.priority_scores),
        )
        .filter(Complaint.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    result = [_build_complaint_response(c, db) for c in complaints]
    set_cached_data(cache_key, [r.model_dump(mode="json") for r in result])
    return result


@router.get("", response_model=list[ComplaintResponse])
def list_complaints(
    db: Annotated[Session, Depends(get_db)],
    complexity: str | None = Query(
        None,
        description="Optional filter by criticality level: LOW, MEDIUM, HIGH, CRITICAL (or low, med, high, critical)",
    ),
    skip: int = 0,
    limit: int = 100,
):
    """
    List complaints with optional criticality/complexity filtering:
    - GET /api/v1/complaints (Returns all tickets)
    - GET /api/v1/complaints?complexity=CRITICAL (Returns critical tickets)
    """
    comp_filter = complexity.strip().lower() if complexity else "all"
    cache_key = f"complaints:all:{comp_filter}"
    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    query = db.query(Complaint).options(
        joinedload(Complaint.complaint_address),
        joinedload(Complaint.ai_analysis),
        joinedload(Complaint.priority_scores),
    )
    if complexity:
        norm = COMPLEXITY_MAP.get(
            complexity.strip().lower(), complexity.strip().upper()
        )
        query = query.join(Complaint.priority_scores).filter(
            ComplaintPriorityScores.complexity == norm
        )

    complaints = query.offset(skip).limit(limit).all()
    result = [_build_complaint_response(c, db) for c in complaints]
    set_cached_data(cache_key, [r.model_dump(mode="json") for r in result])
    return result


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    cache_key = f"complaint:{complaint_id}"
    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    complaint = (
        db.query(Complaint)
        .options(
            joinedload(Complaint.complaint_address),
            joinedload(Complaint.ai_analysis),
            joinedload(Complaint.priority_scores),
        )
        .filter(Complaint.id == complaint_id)
        .first()
    )
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with ID '{complaint_id}' not found",
        )
    result = _build_complaint_response(complaint, db)
    set_cached_data(cache_key, result.model_dump(mode="json"))
    return result
