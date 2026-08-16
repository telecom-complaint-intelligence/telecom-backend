# 📡 Integration 3: Complaint Lifecycle, Cache Memory & Route Protection Flow

This document details the architecture, flows, and implementation choices for the **Integration 3** iteration of the Telu Telecom Triage system.

---

## 🏗️ 1. Complete End-to-End Triage & Resolution Flow

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer Portal
    participant Backend as telecom-backend (:8000)
    participant Redis as Redis Cache
    participant DB as PostgreSQL DB
    participant AI as telecom-ai-service (:8001)

    Customer->>Backend: POST /api/v1/complaints/me {"complaint": "wifi drop..."}
    Note over Backend: Validate payload & trigger AI Inference
    Backend->>AI: POST /api/v1/analyze {"complaint": "wifi drop..."}
    AI-->>Backend: Return AI features & RAG response (Solution, neg/pos sentiment, severity)
    
    Backend->>DB: Save in normalized tables (complaints, address, ai_analysis, priority)
    Note over Backend: Auto-invalidate Redis caches: user:{user_id}:complaints & complaints:all*
    Backend->>Redis: Invalidate keys
    Backend-->>Customer: Return Ticket ID and Triage Info (HTTP 201)

    Note over Customer: Stream multi-stage loader (Sentiment, Tech Info, Severity)
    
    alt Severity is LOW or MEDIUM
        Customer->>Customer: Display AI Solution ("Unplug router for 30s...")
        alt Issue Solved
            Customer->>Backend: PATCH /api/v1/complaints/{id} {"status": "CLOSED"}
            Backend->>Redis: Invalidate complaint:{id} & user:{user_id}:complaints
            Backend->>DB: Update status to CLOSED
        else Issue Persists
            Customer->>Customer: Render follow-up textbox
            Customer->>Backend: PATCH /api/v1/complaints/{id} {"complaint2": "rebooted but still dead", "status": "IN_PROGRESS"}
            Backend->>Redis: Invalidate caches
            Backend->>DB: Update status to IN_PROGRESS & save complaint2
        end
    else Severity is HIGH or CRITICAL
        Customer->>Customer: Bypass local checks. Display Technician dispatch update.
    end
```

---

## ⚡ 2. Redis Caching & Invalidation Architecture

To deliver sub-millisecond retrieval speeds, we implemented caching middleware at the API router layer:

```mermaid
flowchart TD
    Request["GET /api/v1/complaints/me"] --> CheckCache{"Key user:user_id:complaints exists?"}
    CheckCache -- Yes --> ReturnCache["Return cached JSON list (Sub-millisecond)"]
    CheckCache -- No --> FetchDB["Fetch normalized tables from DB"]
    FetchDB --> SaveCache["Cache list in Redis for 300s"]
    SaveCache --> ReturnResponse["Return HTTP 200 Response"]

    WriteAction["POST /me or PATCH /{id}"] --> SaveDB["Commit transaction to DB"]
    SaveDB --> ClearCache["Delete keys: complaint:id, user:user_id:complaints, complaints:all*"]
    ClearCache --> ReturnWrite["Return HTTP 201/200"]
```

---

## 🔒 3. Route Protection & Onboarding Verification Gates

The Next.js frontend is secured via edge middleware and onboarding validators:

```mermaid
flowchart TD
    UserRequest["User navigates to route"] --> CheckToken{"Is telu_token cookie present?"}
    CheckToken -- No --> CheckAuth{"Is route /auth*?"}
    CheckAuth -- Yes --> Allow["Allow access"]
    CheckAuth -- No --> RedirectLogin["Redirect to /auth (Login)"]

    CheckToken -- Yes --> CheckRole{"Is role correct for route?"}
    CheckRole -- No --> RedirectAuth["Redirect to /auth (Incorrect Role)"]
    CheckRole -- Yes --> OnboardingCheck{"Is route /auth/setup-profile or /auth/verify-email?"}
    
    OnboardingCheck -- Yes --> Allow
    OnboardingCheck -- No --> ProfileComplete{"Is user.isProfileComplete == True?"}
    ProfileComplete -- Yes --> Allow
    ProfileComplete -- No --> RedirectProfile["Redirect to /auth/setup-profile"]
```

---

## 📝 4. Completed Tasks in Iteration 3

1. **API Compatibility & Fixes**:
   - Fixed schema name mismatch by allowing `complaint` or `complaint1` in Pydantic schema using `AliasChoices` validator.
   - Fixed the backend `/auth/complete-profile` route to save `plan_usage` into `service_details` table.
2. **Caching Implementation**:
   - Cached individual ticket detail (`complaint:{id}`), customer complaints (`user:{user_id}:complaints`), and global list queries (`complaints:all:{complexity}`).
   - Enabled auto-invalidation on POST and PATCH operations.
3. **Frontend Integration**:
   - Implemented dynamic customer sidebar fetching login data (`Vaaheesan S` / `CUST-S2JX5LX` etc.).
   - Added low-severity resolution checker asking if the issue is solved, with inline text box to submit `complaint2` follow-up.
   - Synchronized plan usage setting to reflect onboarding selections.
4. **Build & Quality Controls**:
   - Configured Next.js middleware router rules.
   - Fixed TypeScript static-generation type mismatch errors.
