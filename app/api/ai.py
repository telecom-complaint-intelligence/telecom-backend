import os
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai", tags=["AI & Agents Proxy"])

AI_SERVICE_BASE_URL = os.getenv("AI_SERVICE_BASE_URL", "http://localhost:8001/api/v1")


class AnalyzeProxyRequest(BaseModel):
    complaint: str = Field(..., min_length=3, description="Complaint text to analyze")


class SolutionProxyRequest(BaseModel):
    complaint: str
    complaint_id: str | None = "AUTO"
    complexity: str | None = "LOW"
    category: str | None = "Internet / Connectivity"
    technical_information: dict[str, Any] | str | None = None


class EscalateProxyRequest(BaseModel):
    complaint: str
    previous_solution: str | None = ""
    customer_feedback: bool | str = Field(
        ...,
        description="True/False or description indicating if previous solution worked",
    )
    current_severity: str | None = "LOW"
    complexity: str | None = "LOW"
    category: str | None = "General"
    technical_information: dict[str, Any] | str | None = None


class HighProxyRequest(BaseModel):
    complaint: str
    complaint_text: str | None = None
    complexity: str | None = "CRITICAL"
    scope: str | None = "area"
    duration_hours: float | None = 24.0
    severity: str | None = "high"
    technical_information: dict[str, Any] | str | None = None


@router.post("/analyze")
def proxy_analyze_complaint(payload: AnalyzeProxyRequest) -> dict[str, Any]:
    """
    Directly invokes telecom-ai-service Master Inference & Multi-Agent triage:
    - DistilBERT classification
    - RoBERTa sentiment
    - Hybrid Information Extraction
    - Priority & Complexity calculation
    - Automatic dispatch to Solution Agent (LOW/MED) or High Agent (HIGH/CRITICAL).
    """
    url = f"{AI_SERVICE_BASE_URL}/analyze"
    try:
        with httpx.Client(timeout=35.0) as client:
            resp = client.post(url, json={"complaint": payload.complaint})
            if resp.status_code == 200:
                return resp.json()
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"AI Service error: {resp.text}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to reach telecom-ai-service at {url}: {e!s}",
        )


@router.post("/solution")
def proxy_solution_agent(payload: SolutionProxyRequest) -> dict[str, Any]:
    """
    Directly invokes the Solution Agent in telecom-ai-service to generate self-care instructions.
    """
    url = f"{AI_SERVICE_BASE_URL}/agents/solution"
    try:
        with httpx.Client(timeout=35.0) as client:
            resp = client.post(url, json=payload.model_dump(mode="json"))
            if resp.status_code == 200:
                return resp.json()
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"AI Service error: {resp.text}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to reach telecom-ai-service at {url}: {e!s}",
        )


@router.post("/escalate")
def proxy_escalation_agent(payload: EscalateProxyRequest) -> dict[str, Any]:
    """
    Directly invokes the Escalation Agent in telecom-ai-service based on customer feedback.
    """
    url = f"{AI_SERVICE_BASE_URL}/agents/escalate"
    try:
        with httpx.Client(timeout=35.0) as client:
            resp = client.post(url, json=payload.model_dump(mode="json"))
            if resp.status_code == 200:
                return resp.json()
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"AI Service error: {resp.text}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to reach telecom-ai-service at {url}: {e!s}",
        )


@router.post("/high")
def proxy_high_agent(payload: HighProxyRequest) -> dict[str, Any]:
    """
    Directly invokes the High Agent 5-Agent Council in telecom-ai-service.
    """
    url = f"{AI_SERVICE_BASE_URL}/agents/high"
    try:
        with httpx.Client(timeout=35.0) as client:
            resp = client.post(url, json=payload.model_dump(mode="json"))
            if resp.status_code == 200:
                return resp.json()
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"AI Service error: {resp.text}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to reach telecom-ai-service at {url}: {e!s}",
        )
