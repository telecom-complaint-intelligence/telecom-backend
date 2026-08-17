import os
import sys
import uuid

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.core.security import create_access_token
from app.main import app
from app.models.user import Profile, User

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_guest_complaint_on_behalf_with_custom_address():
    payload = {
        "complaint1": "Our fiber cable is damaged by heavy construction, leaving multiple users without internet service.",
        "filling_on_behalf_of": True,
        "address": "77 Sector B, Anna Nagar",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "zipcode": "600040",
    }

    response = client.post("/api/v1/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()

    # Core Complaint fields
    assert "id" in data
    assert data["user_id"] is None
    assert data["ticket_number"] is not None
    assert data["ticket_number"].startswith("TICK-")
    assert data["complaint1"] == payload["complaint1"]
    assert data["filling_on_behalf_of"] is True
    assert data["status"] == "OPEN"
    assert data["response"] is not None

    # Custom Address Table (complaint_address)
    assert data["complaint_address"] is not None
    assert data["complaint_address"]["city"] == "Chennai"
    assert data["complaint_address"]["zipcode"] == "600040"
    assert data["resolved_address"]["city"] == "Chennai"

    # AI & Priority
    assert data["ai_analysis"] is not None
    assert data["priority_scores"] is not None


def test_create_authenticated_complaint_for_self_resolves_profile_address():
    db = SessionLocal()
    test_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
    user = User(
        email=test_email,
        role="customer",
        customer_id=f"CUST-{uuid.uuid4().hex[:8].upper()}",
        email_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = Profile(
        user_id=user.id,
        name="Priya Sharma",
        phone="9876543210",
        address="10 Marina Beach Rd",
        city="Chennai",
        state_val="Tamil Nadu",
        country="India",
        zipcode="600001",
        is_complete=True,
    )
    db.add(profile)
    db.commit()

    token = create_access_token(data={"sub": user.email, "role": user.role})

    # Filing for SELF (filling_on_behalf_of = False, no address in payload)
    payload_self = {
        "complaint1": "Broadband optical signal is red on my ONT router.",
        "filling_on_behalf_of": False,
    }
    resp = client.post(
        "/api/v1/complaints/me",
        json=payload_self,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"] == user.id
    assert data["filling_on_behalf_of"] is False
    assert data["complaint_address"] is None  # No custom address row needed

    # Dynamic Address resolution from User Profile
    assert data["resolved_address"] is not None
    assert data["resolved_address"]["city"] == "Chennai"
    assert data["resolved_address"]["state"] == "Tamil Nadu"
    assert data["resolved_address"]["zipcode"] == "600001"

    # Test PATCH to add complaint2 & mark RESOLVED
    patch_resp = client.patch(
        f"/api/v1/complaints/{data['id']}",
        json={
            "complaint2": "Technician visited and spliced the fiber, light is now green.",
            "status": "RESOLVED",
        },
    )
    assert patch_resp.status_code == 200
    patched_data = patch_resp.json()
    assert patched_data["complaint2"] is not None
    assert patched_data["status"] == "RESOLVED"
    assert patched_data["closing_time_stamp"] is not None

    db.close()


def test_post_complaints_me_unauthorized_without_token():
    payload = {"complaint1": "Testing unauthenticated call to /me"}
    resp = client.post("/api/v1/complaints/me", json=payload)
    assert resp.status_code == 401


def test_list_complaints_endpoint():
    response = client.get("/api/v1/complaints")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_complaints_with_complexity_filter():
    response = client.get("/api/v1/complaints?complexity=CRITICAL")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["priority_scores"]["complexity"] == "CRITICAL"


def test_get_critical_complaints_feed_sorted():
    response = client.get("/api/v1/complaints/critical")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    scores = [item["priority_scores"]["total_complexity_score"] for item in data]
    # Check sorted descending
    assert scores == sorted(scores, reverse=True)


def test_submit_complaint_feedback_true_resolves():
    # 1. Create a complaint
    payload = {"complaint1": "My wifi connection drops intermittently"}
    create_resp = client.post("/api/v1/complaints", json=payload)
    assert create_resp.status_code == 201
    complaint_id = create_resp.json()["id"]

    # 2. Submit Feedback True
    fb_resp = client.post(
        f"/api/v1/complaints/{complaint_id}/feedback",
        json={"customer_feedback": True},
    )
    assert fb_resp.status_code == 200
    data = fb_resp.json()
    assert data["customer_feedback"] is True
    assert data["status"] == "RESOLVED"
    assert data["closing_time_stamp"] is not None


def test_submit_complaint_feedback_false_escalates():
    # 1. Create a complaint
    payload = {
        "complaint1": "Optical loss error LOS light blinking red continuously",
        "filling_on_behalf_of": False,
    }
    create_resp = client.post("/api/v1/complaints", json=payload)
    assert create_resp.status_code == 201
    complaint_id = create_resp.json()["id"]

    # 2. Submit Feedback False (solution didn't work)
    fb_resp = client.post(
        f"/api/v1/complaints/{complaint_id}/feedback",
        json={"customer_feedback": False},
    )
    assert fb_resp.status_code == 200
    data = fb_resp.json()
    assert data["customer_feedback"] is False
    assert data["status"] == "ESCALATED"
    assert data["ai_analysis"] is not None
    assert (
        data["ai_analysis"]["solution_high"] is not None or data["response"] is not None
    )
