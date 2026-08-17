from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_proxy_ai_analyze():
    response = client.post(
        "/api/v1/ai/analyze",
        json={"complaint": "Internet connection drops every evening around 8pm"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "complexity" in data
    assert "total_complexity_score" in data


def test_proxy_ai_solution():
    response = client.post(
        "/api/v1/ai/solution",
        json={
            "complaint": "Broadband router shows orange light on LOS",
            "complexity": "LOW",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert (
        "customer_instructions" in data
        or "summary" in data
        or "recommended_actions" in data
    )


def test_proxy_ai_escalate():
    response = client.post(
        "/api/v1/ai/escalate",
        json={
            "complaint": "Optical fiber cut during road construction",
            "previous_solution": "1. Restart router",
            "customer_feedback": False,
            "current_severity": "LOW",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "escalated" in data
    assert "next_severity" in data


def test_proxy_ai_high():
    response = client.post(
        "/api/v1/ai/high",
        json={
            "complaint": "Area network tower physical damage and complete blackout",
            "complexity": "CRITICAL",
            "scope": "area",
            "duration_hours": 72.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "diagnosis" in data or "proposed_action" in data or "priority" in data
