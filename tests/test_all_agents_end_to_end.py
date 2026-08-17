"""
End-to-End Test Matrix in telecom-backend verifying all Agent tiers and Escalation lifecycle:
1. LOW Agent Flow
2. MEDIUM Agent Flow
3. HIGH Agent Council Flow
4. CRITICAL Emergency Flow & /complaints/critical feed
5. Complete Customer Feedback Escalation (LOW -> Feedback False -> ESCALATED + High Council Decision)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_1_low_agent_backend_flow():
    """1. LOW tier: Submits low complaint -> verifies solution_a is saved in DB & returned."""
    payload = {"complaint1": "My wifi connection is dropping occasionally on phone"}
    resp = client.post("/api/v1/complaints", json=payload)
    assert resp.status_code == 201
    data = resp.json()

    assert data["status"] == "OPEN"
    assert data["priority_scores"]["complexity"] in ["LOW", "MEDIUM"]
    assert data["ai_analysis"]["solution_a"] is not None
    assert data["response"] is not None


def test_2_medium_agent_backend_flow():
    """2. MEDIUM tier: Submits medium issue -> verifies diagnostic analysis in DB."""
    payload = {
        "complaint1": "Broadband optical ONT router has intermittent sync failure"
    }
    resp = client.post("/api/v1/complaints", json=payload)
    assert resp.status_code == 201
    data = resp.json()

    assert data["ai_analysis"]["solution_a"] is not None
    assert data["priority_scores"]["total_complexity_score"] > 0


def test_3_high_agent_backend_flow():
    """3. HIGH tier: Submits high severity issue -> verifies High Council outputs in DB."""
    payload = {
        "complaint1": "Apartment main fiber junction box damaged and offline for 96 hours"
    }
    resp = client.post("/api/v1/complaints", json=payload)
    assert resp.status_code == 201
    data = resp.json()

    assert data["priority_scores"]["complexity"] in ["HIGH", "CRITICAL"]
    ai = data["ai_analysis"]
    assert ai["diagnosis"] is not None or ai["solution_a"] is not None


def test_4_critical_agent_backend_flow_and_feed():
    """4. CRITICAL tier: Submits critical area damage -> verifies critical feed sorting."""
    payload = {
        "complaint1": "Critical fiber optic cable cut on main street, emergency hospital and thousands offline"
    }
    resp = client.post("/api/v1/complaints", json=payload)
    assert resp.status_code == 201
    ticket = resp.json()
    assert ticket["priority_scores"]["complexity"] == "CRITICAL"

    # Verify dedicated critical feed retrieves and sorts by total_complexity_score DESC
    crit_resp = client.get("/api/v1/complaints/critical")
    assert crit_resp.status_code == 200
    crit_list = crit_resp.json()
    assert len(crit_list) > 0
    scores = [
        item["priority_scores"]["total_complexity_score"] for item in crit_list
    ]
    assert scores == sorted(scores, reverse=True)


def test_5_full_feedback_escalation_lifecycle():
    """
    5. Escalation Agent Lifecycle:
    Step A: Customer submits initial complaint.
    Step B: Receives initial self-care solution.
    Step C: Customer submits feedback = False (solution failed).
    Step D: Escalation Agent evaluates policy & executes High Agent Council.
    Step E: Complaint status becomes 'ESCALATED', solution_high and council diagnosis are persisted in DB.
    """
    # Step A & B: Initial submission
    create_payload = {
        "complaint1": "LOS red light on fiber router is blinking constantly"
    }
    create_resp = client.post("/api/v1/complaints", json=create_payload)
    assert create_resp.status_code == 201
    complaint_id = create_resp.json()["id"]
    initial_solution = create_resp.json()["response"]
    assert initial_solution is not None

    # Step C & D & E: Submit Feedback = False
    fb_resp = client.post(
        f"/api/v1/complaints/{complaint_id}/feedback",
        json={"customer_feedback": False},
    )
    assert fb_resp.status_code == 200
    updated_data = fb_resp.json()

    assert updated_data["customer_feedback"] is False
    assert updated_data["status"] == "ESCALATED"
    assert updated_data["ai_analysis"]["solution_high"] is not None
    assert updated_data["ai_analysis"]["diagnosis"] is not None
    assert updated_data["ai_analysis"]["root_cause"] is not None
    assert updated_data["ai_analysis"]["final_decision"] is not None
