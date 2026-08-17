import os
from typing import Any, Dict, Optional, Union
import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ai", tags=["AI & Agents Proxy"])

AI_SERVICE_BASE_URL = os.getenv(
    "AI_SERVICE_BASE_URL", "http://localhost:8001/api/v1"
)


class AnalyzeProxyRequest(BaseModel):
    complaint: str = Field(..., min_length=3, description="Complaint text to analyze")


class SolutionProxyRequest(BaseModel):
    complaint: str
    complaint_id: Optional[str] = "AUTO"
    complexity: Optional[str] = "LOW"
    category: Optional[str] = "Internet / Connectivity"
    technical_information: Optional[Union[Dict[str, Any], str]] = None


class EscalateProxyRequest(BaseModel):
    complaint: str
    previous_solution: Optional[str] = ""
    customer_feedback: Union[bool, str] = Field(
        ...,
        description="True/False or description indicating if previous solution worked",
    )
    current_severity: Optional[str] = "LOW"
    complexity: Optional[str] = "LOW"
    category: Optional[str] = "General"
    technical_information: Optional[Union[Dict[str, Any], str]] = None


class HighProxyRequest(BaseModel):
    complaint: str
    complaint_text: Optional[str] = None
    complexity: Optional[str] = "CRITICAL"
    scope: Optional[str] = "area"
    duration_hours: Optional[float] = 24.0
    severity: Optional[str] = "high"
    technical_information: Optional[Union[Dict[str, Any], str]] = None


@router.post("/analyze")
def proxy_analyze_complaint(payload: AnalyzeProxyRequest) -> Dict[str, Any]:
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
            detail=f"Unable to reach telecom-ai-service at {url}: {str(e)}",
        )


@router.post("/solution")
def proxy_solution_agent(payload: SolutionProxyRequest) -> Dict[str, Any]:
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
            detail=f"Unable to reach telecom-ai-service at {url}: {str(e)}",
        )


@router.post("/escalate")
def proxy_escalation_agent(payload: EscalateProxyRequest) -> Dict[str, Any]:
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
            detail=f"Unable to reach telecom-ai-service at {url}: {str(e)}",
        )


@router.post("/high")
def proxy_high_agent(payload: HighProxyRequest) -> Dict[str, Any]:
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
            detail=f"Unable to reach telecom-ai-service at {url}: {str(e)}",
        )
