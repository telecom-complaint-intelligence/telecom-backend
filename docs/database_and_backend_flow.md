# Database Architecture & Backend Workflow Documentation

This document describes the normalized PostgreSQL database structure, caching policies, and backend/frontend authentication/configuration flows for the Telu Telecom Triage enterprise system.

---

## 1. Database Schema Structure

The database is built using SQLAlchemy and PostgreSQL, adhering to 3NF normalization for enterprise scalability.

```mermaid
erDiagram
    users ||--|| profiles : "one-to-one (user_id)"
    users ||--|| service_details : "one-to-one (user_id)"
    users ||--o| departments : "many-to-one (department_id)"
    users ||--o{ complaints : "one-to-many (user_id)"
    client_invitations ||--o| departments : "many-to-one (department_id)"
    complaints ||--o| complaint_address : "one-to-one (complaint_id)"
    complaints ||--|| complaint_ai_analysis : "one-to-one (complaint_id)"
    complaints ||--|| complaint_priority_scores : "one-to-one (complaint_id)"

    users {
        VARCHAR(36) id PK
        VARCHAR(50) customer_id UK
        VARCHAR(255) email UK
        VARCHAR(255) hashed_password
        VARCHAR(50) role
        BOOLEAN email_verified
        BOOLEAN cookie_consent
        BOOLEAN is_archived
        VARCHAR(36) department_id FK
        TIMESTAMP created_at
        VARCHAR(6) verification_otp
        TIMESTAMP otp_created_at
    }
    profiles {
        VARCHAR(36) id PK
        VARCHAR(36) user_id FK
        VARCHAR(255) name
        VARCHAR(50) phone
        TEXT profile_picture
        VARCHAR(255) address
        VARCHAR(100) city
        VARCHAR(100) state_val
        VARCHAR(100) country
        VARCHAR(20) zipcode
        BOOLEAN is_complete
    }
    service_details {
        VARCHAR(36) id PK
        VARCHAR(36) user_id FK
        VARCHAR(50) account_ref
        VARCHAR(50) bill_cycle
        VARCHAR(100) active_plan
        VARCHAR(50) connection_status
        VARCHAR(50) plan_usage
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
        VARCHAR(36) user_id FK
        TEXT complaint1
        TEXT response
        TEXT complaint2
        BOOLEAN customer_feedback
        BOOLEAN filling_on_behalf_of
        VARCHAR(50) status
        VARCHAR(100) category
        VARCHAR(50) resolved_by
        TIMESTAMP timestamp
        TIMESTAMP created_at
        TIMESTAMP response_timestamp
        TIMESTAMP follow_up_timestamp
        TIMESTAMP closing_time_stamp
    }
    complaint_address {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK
        TEXT address
        VARCHAR(100) city
        VARCHAR(100) state
        VARCHAR(100) country
        VARCHAR(20) zipcode
    }
    complaint_ai_analysis {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK
        FLOAT category_confidence
        FLOAT negativity_score
        FLOAT sentiment_score
        JSON component
        JSON failure_type
        VARCHAR(50) scope
        VARCHAR(50) service_impact
        FLOAT duration_hours
        VARCHAR(50) occurrence_pattern
        TEXT solution_a
        TEXT solution_high
        JSON warnings
        JSON evidence
        FLOAT confidence_score
        VARCHAR(255) diagnosis
        TEXT root_cause
        VARCHAR(50) risk_level
        VARCHAR(50) policy_status
        VARCHAR(100) final_decision
        TEXT critic_feedback
        TEXT reasoning
        VARCHAR(50) extraction_source
        FLOAT lowest_confidence
        TIMESTAMP created_at
    }
    complaint_priority_scores {
        VARCHAR(36) id PK
        VARCHAR(36) complaint_id FK
        VARCHAR(50) complexity
        INTEGER complexity_score
        FLOAT weighted_complexity_score
        FLOAT weighted_negativity_score
        FLOAT total_complexity_score
        TIMESTAMP created_at
    }
```

### Table 1: `users` (Core Auth & Settings)
Stores credentials, verification status, and department mappings.
* `id` (VARCHAR(36), PK): Unique internal UUID.
* `customer_id` (VARCHAR(50), UK): Public Unique Alphanumeric reference (e.g. `OPS-N7QMVBV0` or `CUST-7F3A9D12`).
* `email` (VARCHAR, UK, Not Null): User login email.
* `hashed_password` (VARCHAR, Nullable): Password hash.
* `role` (VARCHAR, Not Null): Access level (`customer`, `client`).
* `email_verified` (BOOLEAN, Not Null): Verified status.
* `cookie_consent` (BOOLEAN, Not Null): Tracks cookie policy acceptance.
* `is_archived` (BOOLEAN, Not Null, Default `False`): Handles soft-deletion.
* `department_id` (VARCHAR(36), FK): Reference to `departments.id`.
* `created_at` (TIMESTAMP, Not Null): Account signup timestamp.
* `verification_otp` (VARCHAR(6), Nullable): Current email OTP.
* `otp_created_at` (TIMESTAMP, Nullable): Code generation timestamp.

### Table 2: `profiles` (Contact & Location Details)
Stores billing and service installation contact parameters.
* `id` (VARCHAR(36), PK): Profile UUID.
* `user_id` (VARCHAR(36), FK): References parent user profile.
* `name` (VARCHAR, Nullable): Billing name.
* `phone` (VARCHAR, Nullable): Contact phone.
* `profile_picture` (VARCHAR, Nullable): Avatar URL.
* `address` (VARCHAR, Nullable): Installation address.
* `city` (VARCHAR, Nullable): Installation city.
* `state_val` (VARCHAR, Nullable): Installation state.
* `country` (VARCHAR, Nullable, Default `"India"`): Installation country.
* `zipcode` (VARCHAR, Nullable): Installation postal code.
* `is_complete` (BOOLEAN, Not Null, Default `False`): Profile complete status.

### Table 3: `service_details` (Subscription & Plans)
Tracks enterprise connection line status, account references, and bandwidth details.
* `id` (VARCHAR(36), PK): Service details UUID.
* `user_id` (VARCHAR(36), FK): References parent user.
* `account_ref` (VARCHAR, Nullable): Customer account number.
* `bill_cycle` (VARCHAR, Nullable): Billing cycle day reference.
* `active_plan` (VARCHAR, Nullable): Current plan title (e.g., `Fibre 100 Mbps`).
* `connection_status` (VARCHAR, Nullable): Status (`Active`, `Suspended`, `Inactive`).
* `plan_usage` (VARCHAR, Nullable): Usage tier (`self`, `shop`, `organization`).

### Table 4: `departments` (Custom Work Groups)
Configurable work departments managed strictly by the Master Client.
* `id` (VARCHAR(36), PK): Department UUID.
* `name` (VARCHAR(100), UK, Not Null): Department title (e.g., `Business Analyst`).
* `is_archived` (BOOLEAN, Not Null, Default `False`): Soft-archiving status.
* `created_at` (TIMESTAMP, Not Null): Creation timestamp.

### Table 5: `client_invitations` (Client Onboarding Tracking)
Tracks invited staff operators, passwords, and validation tokens.
* `id` (VARCHAR(36), PK): Invitation UUID.
* `email` (VARCHAR, Not Null): Target email.
* `hashed_password` (VARCHAR, Not Null): Temporary password.
* `token` (VARCHAR, UK, Not Null): Unique secure activation token.
* `is_activated` (BOOLEAN, Not Null, Default `False`): Activation toggle.
* `department_id` (VARCHAR(36), FK): Target department reference.
* `created_at` (TIMESTAMP, Not Null): Invitation timestamp.
* `expires_at` (TIMESTAMP, Nullable): Token expiration timestamp.

### Table 6: `complaints` (Customer Tickets)
Stores primary customer issue reports, statuses, and follow-ups.
* `id` (VARCHAR(36), PK): Unique ticket UUID.
* `ticket_number` (VARCHAR(50), UK): Public tracking number.
* `user_id` (VARCHAR(36), FK): References user who submitted the ticket.
* `complaint1` (TEXT, Not Null): First complaint description text.
* `response` (TEXT, Nullable): Action/Proposed solution text from technicians.
* `complaint2` (TEXT, Nullable): Follow-up complaint text from customer.
* `customer_feedback` (BOOLEAN, Nullable): Confirmation of whether the proposed solution worked.
* `filling_on_behalf_of` (BOOLEAN, Not Null, Default `False`): Toggles custom address override.
* `status` (VARCHAR(50), Not Null, Default `"OPEN"`): Ticket lifecycle status (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`).
* `category` (VARCHAR(100), Nullable): AI classified complaint category.
* `resolved_by` (VARCHAR(50), Nullable): Team member or agent who resolved the issue.
* `timestamp` (TIMESTAMP, Not Null): Submission time.
* `created_at` (TIMESTAMP, Not Null): Creation timestamp.
* `response_timestamp` (TIMESTAMP, Nullable): Proposed solution timestamp.
* `follow_up_timestamp` (TIMESTAMP, Nullable): Follow-up submission timestamp.
* `closing_time_stamp` (TIMESTAMP, Nullable): Resolved/Closed timestamp.

### Table 7: `complaint_address` (Custom Installation Locations)
Stores custom installation location details when a complaint is filed on behalf of someone else.
* `id` (VARCHAR(36), PK): Address UUID.
* `complaint_id` (VARCHAR(36), FK, UK): References parent complaint.
* `address` (TEXT, Nullable): Installation address.
* `city` (VARCHAR(100), Nullable): City.
* `state` (VARCHAR(100), Nullable): State.
* `country` (VARCHAR(100), Not Null, Default `"India"`): Country.
* `zipcode` (VARCHAR(20), Nullable): Postal code.

### Table 8: `complaint_ai_analysis` (AI Triage & Reasoning Logs)
Stores ML/NLP model classifications, confidence scores, technical extraction parameters, and multi-agent reasoning.
* `id` (VARCHAR(36), PK): Analysis UUID.
* `complaint_id` (VARCHAR(36), FK, UK): References parent complaint.
* `category_confidence` (FLOAT, Nullable): Classification confidence.
* `negativity_score` (FLOAT, Nullable): 0 to 1 negativity index.
* `sentiment_score` (FLOAT, Nullable): 0 to 100 sentiment score.
* `component` (JSON, Nullable): Technical system component(s) involved.
* `failure_type` (JSON, Nullable): Extracted technical issue failure types.
* `scope` (VARCHAR(50), Nullable): Outage scale scope (`Individual`, `Neighborhood`, etc.).
* `service_impact` (VARCHAR(50), Nullable): Impact levels (`No Service`, `Degraded Service`).
* `duration_hours` (FLOAT, Nullable): Outage duration.
* `occurrence_pattern` (VARCHAR(50), Nullable): Occurrence logs (`Intermittent`, `Continuous`).
* `solution_a` (TEXT, Nullable): Customer troubleshooting instructions.
* `solution_high` (TEXT, Nullable): Dispatch technician field instructions.
* `warnings` (JSON, Nullable): Core safety/precautionary actions.
* `evidence` (JSON, Nullable): Matched Knowledge Base evidence logs.
* `confidence_score` (FLOAT, Nullable): Global model confidence score.
* `diagnosis` (VARCHAR(255), Nullable): Consensus diagnosis log.
* `root_cause` (TEXT, Nullable): Consensus root cause.
* `risk_level` (VARCHAR(50), Nullable): Operation risk level.
* `policy_status` (VARCHAR(50), Nullable): Compliance status.
* `final_decision` (VARCHAR(100), Nullable): Consensus final action.
* `critic_feedback` (TEXT, Nullable): Multi-agent feedback review.
* `reasoning` (TEXT, Nullable): Complete step-by-step reasoning trace.
* `extraction_source` (VARCHAR(50), Nullable): Processing source engine.
* `lowest_confidence` (FLOAT, Nullable): Configured confidence floor constraint.
* `created_at` (TIMESTAMP, Not Null): Creation timestamp.

### Table 9: `complaint_priority_scores` (Priority Calculation Metrics)
Stores the calculated complexity ratings and priority scores of a complaint.
* `id` (VARCHAR(36), PK): Score record UUID.
* `complaint_id` (VARCHAR(36), FK, UK): References parent complaint.
* `complexity` (VARCHAR(50), Not Null): Final priority tier (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
* `complexity_score` (INTEGER, Not Null): Raw complexity rating.
* `weighted_complexity_score` (FLOAT, Not Null): Weighted technical complexity (85%).
* `weighted_negativity_score` (FLOAT, Not Null): Weighted negativity sentiment (15%).
* `total_complexity_score` (FLOAT, Not Null): Final composite priority score (0-100).
* `created_at` (TIMESTAMP, Not Null): Creation timestamp.

---

## 2. Customer Authentication & Onboarding Workflows

### A. Signup and Verification Sequence
1. **Credentials Registration**: The customer signs up with email and password, posting to `/api/auth/register`.
2. **OTP Dispatched**: The backend creates an empty profile and service details entry, generates a 6-digit OTP code, and dispatches it to the customer's email.
3. **Complexity Rules**:
   * **Length**: Password must be between 8 and 15 characters.
   * **Requirements**: Must include uppercase, lowercase, numbers, and special symbols.
   * **Confirmation**: The confirmation password input field is hidden until all complexity rules turn green.
4. **Verification Gate**: The user is redirected to `/auth/verify-email` and inputs their 6-digit OTP. Submitting calls `POST /api/auth/verify-otp`.
   * **OTP Expiry**: The code expires after 10 minutes.
   * **Spam Prevention**: The resend button is disabled for 120 seconds after being clicked to prevent mail spam.

```mermaid
sequenceDiagram
    participant User as Customer Browser
    participant API as FastAPI Backend
    participant DB as PostgreSQL DB

    User->>API: POST /api/auth/register (email, password)
    API->>DB: Check if email exists
    alt Email already registered
        API-->>User: HTTP 400 Bad Request
    else Email unique
        API->>DB: Generate 6-digit OTP code & Save
        API->>DB: Insert User (email_verified=False)
        API->>DB: Insert Empty Profile & ServiceDetails
        API-->>User: HTTP 200 OK (JWT Token, User Dict)
    end
```

### B. Google OAuth Login Flow (Customer / Master Client)
1. **SSO Dispatch**: Frontend sends client auth tokens to `POST /api/auth/google`.
2. **Authentication**: Backend calls Google API, verifies account, and returns profile details.
3. **Auto-Promotion (Master Client)**: If the email matches `vaahee21@gmail.com`, the system automatically assigns them the `client` role and sets them up as the Master Client Admin.
4. **Name Sync**: Google SSO automatically updates the user's name in the PostgreSQL profile table on every login.

---

## 3. Client Invitation & Activation Workflow

This sequence coordinates invitation dispatching, short URL resolution, landing activation, and OAuth role provisioning for team operators.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Master Client Admin
    participant DB as PostgreSQL Database
    participant API as FastAPI Backend
    actor Operator as Invited Staff Member
    participant Frontend as Next.js App (/auth/activate)

    Admin->>API: POST /api/auth/invite-client (email, password, dept)
    API->>API: Generate secure UUID token
    API->>DB: Store invitation (is_activated=False, hashed_password)
    API->>Operator: Send email with shortlink (http://localhost:8000/api/auth/lnk/{token})
    Operator->>API: Click shortlink (GET /auth/lnk/{token})
    API->>DB: Validate token & activation status
    API-->>Operator: 307 Redirect to Frontend (http://localhost:3000/auth/activate?token={token})
    Operator->>Frontend: Loads activation landing page
    Frontend->>API: POST /api/auth/activate-client (token)
    API->>DB: Toggle is_activated=True & Provision User record
    API-->>Frontend: HTTP 200 OK
    Frontend-->>Operator: Auto-redirect to Login (/auth)
    Operator->>API: Sign-in with Google SSO
    API->>DB: Create/Sync profile name & assign "client" role
    API-->>Operator: Logged in as Master Admin / Operator
```

### A. Link Generation and Redirection
1. **Invite**: The Master Admin specifies details. The backend generates a secure token and hashes credentials in `client_invitations` with `is_activated=False`.
2. **Short-Link**: The email contains `http://localhost:8000/api/auth/lnk/{token}`.
3. **Redirection**: Clicking it hits the backend, which verifies the token and responds with a `307 Redirect` to `http://localhost:3000/auth/activate?token={token}`.
4. **Activation**: The frontend catches the parameter and calls `POST /api/auth/activate-client`, setting `is_activated=True` and creating the initial user in the DB.

### B. Dynamic Role & ID Formatting
* **Header Role display**: If `user.role === "client"` and they belong to a department, they are labeled with their department name appended with `OPS` (e.g. `BUSINESS ANALYST OPS`). Master Client Admins show as `MASTER ADMIN`.
* **ID Formatting**: Client operators' public IDs dynamically display with an `OPS-` prefix (e.g. `OPS-N7QMVBV0`) instead of `CUST-`.

---

## 4. Caching and Resource Archiving

```mermaid
flowchart TD
    A[Client Request: Fetch Operators] --> B{Check Redis Cache}
    B -- Cache Hit --> C[Return Cached JSON]
    B -- Cache Miss --> D[Fetch from PostgreSQL]
    D --> E[Filter out is_archived = True]
    E --> F[Store JSON in Redis]
    F --> G[Return JSON to Client]
    
    H[Admin Request: Update/Delete Operator] --> I[Modify PostgreSQL Database]
    I --> J[Invalidate Cache telu:operators:*]
```

### A. Soft-Delete Archiving
Rather than deleting rows directly, resources utilize the `is_archived` column:
* **Deletion**: Clicking delete calls `DELETE /api/auth/operators/{id}` or `DELETE /api/auth/departments/{id}`, setting `is_archived = True` in the database.
* **Filtering**: Listing endpoints `GET /api/auth/operators` and `GET /api/auth/departments` automatically filter out archived records, hiding them from the UI while preserving historical data.

### B. Fail-Safe Caching (Redis)
* **Key Patterns**: Cached lists are stored in Redis under keys `telu:departments` and `telu:operators:{email}`.
* **Invalidation**: Mutating routes (update, create, delete) automatically trigger invalidation of cache patterns (`telu:operators:*` and `telu:departments`).
* **Resilience**: Redis operations run inside try-catch blocks. If a Redis connection is timed out or unavailable, the backend continues to query the database.

---

## 5. Database Connectivity & Fallback Architecture

The diagram below details how the FastAPI backend establishes connections to the database engine and caching services, including the fail-safe fallbacks for local SQLite and direct DB queries when PostgreSQL or Redis is unreachable.

```mermaid
flowchart TD
    FastAPI[FastAPI Application App/Main] --> InitDB[Init Database Engine app.core.database]
    InitDB --> EnvCheck{DATABASE_URL starts with 'sqlite'? }
    
    EnvCheck -- Yes --> ConnectSQLite[Connect SQLite database]
    EnvCheck -- No --> ConnectPG[Try connecting PostgreSQL]
    
    ConnectPG -- Connection Success --> UsePG[Use PostgreSQL Engine :5433]
    ConnectPG -- Connection Failure --> FallbackSQLite[Use Fallback Local SQLite]
    
    ConnectSQLite --> SQLiteDB[(SQLite DB file: telecom_backend.db)]
    FallbackSQLite --> SQLiteDB
    UsePG --> PostgreSQLDB[(PostgreSQL Database)]

    FastAPI --> InitRedis[Init Redis Client app.core.redis]
    InitRedis --> RedisTry{Connect to Redis?}
    RedisTry -- Success --> CacheActive[Redis Cache Enabled :6379]
    RedisTry -- Failure/Timeout --> CacheInactive[Disable Redis Caching]
    
    CacheActive --> RedisStore[(Redis DB 0)]
    CacheInactive --> DirectDBFallback[Fallback to Direct DB Queries]

    Alembic[Alembic Migrations] --> ConnectPG
    Alembic --> ConnectSQLite
```

