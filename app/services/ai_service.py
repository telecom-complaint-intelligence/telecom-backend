import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001/api/v1/analyze")


class AIServiceClient:
    """
    HTTP Client in telecom-backend for calling the telecom-ai-service inference microservice.
    """

    @staticmethod
    def analyze_complaint(complaint_text: str) -> dict[str, Any]:
        """
        Sends complaint text to telecom-ai-service for classification, sentiment, RAG, and priority.
        """
        try:
            with httpx.Client(timeout=30.0) as client:
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
            "complexity": "MEDIUM",
            "complexity_score": 38,
            "weighted_complexity_score": 32.3,
            "weighted_negativity_score": 4.5,
            "total_complexity_score": 36.8,
        }
