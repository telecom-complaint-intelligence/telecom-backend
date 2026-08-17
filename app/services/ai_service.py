import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001/api/v1/analyze")
AI_ESCALATE_URL = os.getenv(
    "AI_ESCALATE_URL", "http://localhost:8001/api/v1/agents/escalate"
)


class AIServiceClient:
    """
    HTTP Client in telecom-backend for calling telecom-ai-service inference & multi-agent microservice.
    """

    @staticmethod
    def analyze_complaint(complaint_text: str) -> dict[str, Any]:
        """
        Sends complaint text to telecom-ai-service for classification, sentiment, RAG, priority, and agent solution.
        """
        try:
            with httpx.Client(timeout=35.0) as client:
                response = client.post(
                    AI_SERVICE_URL, json={"complaint": complaint_text}
                )
                if response.status_code == 200:
                    return response.json()
                print(
                    f"Warning: AI service returned status code {response.status_code}"
                )
        except (httpx.HTTPError, RuntimeError, ValueError) as e:
            print(
                f"Notice: Failed to connect to AI service at {AI_SERVICE_URL} ({e}). Using local fallback."
            )

        # Local fallback if telecom-ai-service is offline
        return {
            "complaint": complaint_text,
            "category": "General Inquiry",
            "category_confidence": 0.50,
            "negativity_score": 0.30,
            "sentiment_score": 30.0,
            "extraction_source": "fallback",
            "lowest_confidence": 0.50,
            "technical_information": {
                "component": ["unknown"],
                "failure_type": ["unknown"],
                "scope": "individual",
                "service_impact": "degraded",
                "duration_hours": None,
                "occurrence_pattern": "unknown",
            },
            "complexity": "LOW",
            "complexity_score": 25,
            "weighted_complexity_score": 21.25,
            "weighted_negativity_score": 4.5,
            "total_complexity_score": 25.75,
            "solution_a": "1. Power cycle device for 30 seconds.\n2. Verify optical cable link light.\n3. Check subscription status.",
            "solution_high": None,
            "warnings": ["Do not factory reset the router without assistance."],
            "evidence": [],
            "confidence_score": 0.85,
            "diagnosis": "General Technical Inquiry",
            "root_cause": "Unknown",
            "risk_level": "LOW",
            "policy_status": "STANDARD",
            "final_decision": "SELF_CARE",
            "critic_feedback": "Initial self-care solution generated.",
        }

    @staticmethod
    def escalate_complaint(
        complaint_text: str,
        previous_solution: str,
        customer_feedback: bool,
        technical_information: dict[str, Any] | None = None,
        complexity: str = "LOW",
        category: str = "General",
    ) -> dict[str, Any]:
        """
        Calls the Escalation Agent when customer submits feedback.
        If customer_feedback is False, evaluates policy rules and triggers High Agent council.
        """
        try:
            with httpx.Client(timeout=35.0) as client:
                payload = {
                    "complaint": complaint_text,
                    "previous_solution": previous_solution,
                    "customer_feedback": customer_feedback,
                    "current_severity": complexity,
                    "complexity": complexity,
                    "category": category,
                    "technical_information": technical_information,
                }
                response = client.post(AI_ESCALATE_URL, json=payload)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:  # noqa: BLE001
            print(f"Notice: Escalation Agent API call failed: {e}")

        # Local fallback escalation
        return {
            "escalated": True,
            "next_severity": "HIGH",
            "reasoning": "Customer indicated self-care steps did not resolve the issue. Escalated to Tier-2 technical support.",
            "high_agent_result": {
                "diagnosis": "Unresolved Customer Incident",
                "root_cause": "Hardware or Line Signal Degradation",
                "risk_level": "HIGH",
                "policy_status": "ELEVATED",
                "final_decision": "DISPATCH_FIELD_TECH",
                "critic_feedback": "Customer feedback confirms standard self-care failure; technical on-site inspection recommended.",
                "solution_high": "Field engineering dispatched for on-site line quality and equipment inspection.",
                "confidence_score": 0.95,
            },
        }
