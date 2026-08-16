# 📡 Integration 2: Telecom Complaint Intelligence & AI Automated Resolution

This document details the **Integration 2** backend architecture, 3NF normalized PostgreSQL database design, multi-address and on-behalf complaint lifecycle, and the synchronous AI inference pipeline connecting `telecom-backend` to `telecom-ai-service`.

---

## 🏗️ 1. Complete Database Schema (3NF Normalized)

The PostgreSQL database is normalized to 3NF standards, cleanly isolating customer accounts, custom addresses, AI/ML predictions, and priority scoring metrics across dedicated tables.

```mermaid
erDiagram
    users ||--|| profiles : "has profile (user_id)"
    users ||--|| service_details : "has service details (user_id)"
    users ||--o{ complaints : "places (user_id)"
    departments ||--o{ users : "assigns (department_id)"
    departments ||--o{ client_invitations : "invites to (department_id)"
    
    complaints ||--o| complaint_address : "custom address (complaint_id)"
    complaints ||--|| complaint_ai_analysis : "AI triage (complaint_id)"
    complaints ||--|| complaint_priority_scores : "priority math (complaint_id)"

    users {
        VARCHAR(36) id PK
        VARCHAR(50) customer_id UK
        VARCHAR(255) email UK
        VARCHAR(255) hashed_password
        VARCHAR(50) role "customer | client"
        BOOLEAN email_verified
        BOOLEAN cookie_consent
        VARCHAR(36) department_id FK
        VARCHAR(6) verification_otp
        TIMESTAMP otp_created_at
        TIMESTAMP created_at
    }

    profiles {
        VARCHAR(36) id PK
        VARCHAR(36) user_id FK "UK"
        VARCHAR(255) name
        VARCHAR(50) phone
        TEXT address
        VARCHAR(100) city
        VARCHAR(100) state_val
        VARCHAR(100) country "Default: India"
        VARCHAR(20) zipcode
        BOOLEAN is_complete
    }

    service_details {
        VARCHAR(36) id PK
        VARCHAR(36) user_id FK "UK"
        VARCHAR(50) account_ref
        VARCHAR(50) bill_cycle
        VARCHAR(100) active_plan
        VARCHAR(50) connection_status
        VARCHAR(50) plan_usage "self | shop | organization"
    }

    departments {
        VARCHAR(36) id PK
        VARCHAR(100) name UK
        BOOLEAN is_archived
        TIMESTAMP created_at
    }

    client_invitations {
        VARCHAR(36) id PK
        VARCHAR(255) email
        VARCHAR(255) hashed_password
        VARCHAR(255) token UK
        BOOLEAN is_activated
        VARCHAR(36) department_id FK
        TIMESTAMP created_at
        TIMESTAMP expires_at
    }

    complaints {
        VARCHAR(36) id PK
        VARCHAR(50) ticket_number UK
        VARCHAR(36) user_id FK "Nullable (Guest support)"
        TEXT complaint1 "Initial customer complaint text"
        TEXT response "AI automated triage advice / resolution plan"
        TEXT complaint2 "Follow-up complaint / feedback"
        BOOLEAN filling_on_behalf_of "True = custom address, False = user profile"
        VARCHAR(50) status "OPEN | IN_PROGRESS | RESOLVED | CLOSED"
        VARCHAR(100) category "Internet / Connectivity, Billing, etc."
        TIMESTAMP timestamp "Submission timestamp"
        TIMESTAMP created_at
        TIMESTAMP closing_time_stamp "Resolution timestamp"
    }

    complaint_address {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK "UK (1-to-1)"
        TEXT address
        VARCHAR(100) city
        VARCHAR(100) state
        VARCHAR(100) country "Default: India"
        VARCHAR(20) zipcode
    }

    complaint_ai_analysis {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK "UK (1-to-1)"
        FLOAT category_confidence "e.g. 0.9755"
        FLOAT negativity_score "0.0 to 1.0"
        FLOAT sentiment_score "0 to 100"
        JSON component "['fiber_cable', 'router', etc.]"
        JSON failure_type "['physical_damage', 'outage', etc.]"
        VARCHAR(50) scope "individual | multiple_users | area_wide"
        VARCHAR(50) service_impact "complete_outage | degraded | intermittent"
        FLOAT duration_hours
        VARCHAR(50) occurrence_pattern "one_time | recurring"
        TEXT solution_a "AI-suggested technician/user resolution plan"
        VARCHAR(50) extraction_source "ml | llm"
        FLOAT lowest_confidence
        TIMESTAMP created_at
    }

    complaint_priority_scores {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK "UK (1-to-1)"
        VARCHAR(50) complexity "LOW | MEDIUM | HIGH | CRITICAL"
        INTEGER complexity_score "0 to 100 (Technical score)"
        FLOAT weighted_complexity_score "85% weight = score * 0.85"
        FLOAT weighted_negativity_score "15% weight = sentiment * 0.15"
        FLOAT total_complexity_score "weighted_complexity + weighted_negativity"
        TIMESTAMP created_at
    }
```

---

## 🧠 2. End-to-End AI Microservice Integration Pipeline

When a customer submits `complaint1`, `telecom-backend` calls `telecom-ai-service` (`http://localhost:8001/api/v1/analyze`), receiving deep NLP analysis in real time:

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer / Client Portal
    participant Backend as telecom-backend (:8000)
    participant AI as telecom-ai-service (:8001)
    participant DB as PostgreSQL Database (:5433)

    Customer->>Backend: POST /api/v1/complaints (complaint1, filling_on_behalf_of, address)
    Backend->>AI: POST /api/v1/analyze {"complaint": complaint1}
    
    rect rgb(240, 248, 255)
        Note over AI: 1. DistilBERT PyTorch Model → Category & Confidence
        Note over AI: 2. CardiffNLP RoBERTa Model → Negativity (0-1) & Sentiment (0-100)
        Note over AI: 3. Hybrid Extractor (ML + LangGraph LLM Agent) → Tech Info JSON
        Note over AI: 4. Priority Math Engine → 85% Tech Score + 15% Sentiment Score
    end
    
    AI-->>Backend: Return Aggregated AI JSON (Predictions, Solution, Priority)
    
    Backend->>DB: 1. INSERT INTO complaints (complaint1, response, status, etc.)
    alt filling_on_behalf_of == True
        Backend->>DB: 2. INSERT INTO complaint_address (custom location details)
    else filling_on_behalf_of == False
        Backend->>DB: 2. Dynamically references user profiles address
    end
    Backend->>DB: 3. INSERT INTO complaint_ai_analysis (component, solution_a, etc.)
    Backend->>DB: 4. INSERT INTO complaint_priority_scores (complexity, total_score)
    
    DB-->>Backend: Transaction Committed
    Backend-->>Customer: Return HTTP 201 Created (Full Complaint & AI Response)
```

---

## 🔄 3. Multi-Address & On-Behalf Decision Flow

```mermaid
flowchart TD
    Start([Customer Submits Complaint]) --> CheckAuth{Is Bearer Token Provided?}
    CheckAuth -- Yes --> AuthUser[Attach user_id = current_user.id]
    CheckAuth -- No --> GuestUser[Set user_id = null (Guest Mode)]

    AuthUser --> CheckBehalf{Is filling_on_behalf_of == True?}
    GuestUser --> CustomAddr[Save Custom Location into complaint_address Table]

    CheckBehalf -- Yes --> CustomAddr
    CheckBehalf -- No --> ProfileAddr[Auto-Resolve Location from User's profiles Table]

    CustomAddr --> AIAnalysis[Run AI Inference & Save into 3 Normalized Tables]
    ProfileAddr --> AIAnalysis
    AIAnalysis --> End([Return Ticket ID, AI Triage & Resolution Plan])
```

---

## 📈 4. Ticket Lifecycle State Transition

```mermaid
stateDiagram-v2
    [*] --> OPEN: Customer submits complaint1
    OPEN --> IN_PROGRESS: Technician assigned & triage response updated
    IN_PROGRESS --> RESOLVED: Follow-up complaint2 verified & issue fixed (closing_time_stamp recorded)
    RESOLVED --> CLOSED: Customer confirms satisfaction
    CLOSED --> [*]
```

---

## 🌐 5. Microservices & Ports Overview

| Service | Port | Base URL | Swagger UI Interactive Docs |
|---|---|---|---|
| **`telecom-backend`** (FastAPI Core & Auth) | **`8000`** | [http://localhost:8000](http://localhost:8000) | 📘 [http://localhost:8000/docs](http://localhost:8000/docs) |
| **`telecom-ai-service`** (Stateless AI Microservice) | **`8001`** | [http://localhost:8001](http://localhost:8001) | 🤖 [http://localhost:8001/docs](http://localhost:8001/docs) |
| **PostgreSQL Database** (Docker Container) | **`5433`** | `127.0.0.1:5433` | `telecom_db` (User: `postgres` / Pass: `password`) |

---

## 🚀 6. Core API Endpoints

### 🔐 Authentication & Onboarding
* `POST /api/auth/register` — Register customer with email & password (dispatches OTP).
* `POST /api/auth/verify-otp` — Verify 6-digit email OTP.
* `POST /api/auth/login` — Standard credentials login (returns JWT Bearer token).
* `POST /api/auth/google` — Google OAuth SSO authentication.
* `POST /api/auth/complete-profile` — Complete customer contact and installation address.
* `POST /api/auth/service-details` — Update broadband active plan & connection status.

### 📋 Complaints & AI Triage
* `POST /api/v1/complaints` — General complaint intake with `filling_on_behalf_of` toggle.
* `POST /api/v1/complaints/me` — Authenticated complaint intake (auto-links `user_id`).
* `GET /api/v1/complaints/me` — Fetches logged-in customer's tickets with auto-resolved profile address.
* `GET /api/v1/complaints` — Lists all system complaints (supports `?complexity=CRITICAL`).
* `GET /api/v1/complaints/{id}` — Fetches complete normalized ticket details with nested AI analysis.
* `PATCH /api/v1/complaints/{id}` — Submits follow-up `complaint2`, updates `status`, and auto-sets `closing_time_stamp`.
