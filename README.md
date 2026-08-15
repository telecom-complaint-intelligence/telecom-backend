# telecom-backend

FastAPI backend for the Telecom Complaint Intelligence & Automated Resolution Assistant — owns business logic, auth, database, ticket lifecycle, and orchestrates calls to `telecom-ai-service` for classification, sentiment, RAG, and agentic triage.

---

## 🐳 Quick Start (Docker-Only Setup)

You do **not** need to install Python, Uvicorn, or PostgreSQL on your local machine. You can run both the database and the backend application completely inside Docker containers.

### 1. Configure Environment Variables
Create a `.env` file in the root directory (`telecom-backend/`) using `.env.example` as a template:
```bash
cp .env.example .env
```
Open `.env` and fill in your details:
* Google Client ID credentials
* Google SMTP Relay configurations for real email OTP delivery

### 2. Start the Backend & Database
Build the images and start the services in the background or attached mode:
```bash
# Build and run the containers
docker compose up --build

# To run in detached mode (background)
docker compose up -d --build
```
This single command automatically:
1. Starts the PostgreSQL PGVector database container.
2. Starts the FastAPI backend container.
3. Waits for the database to accept connections.
4. **Applies all database migrations (`alembic upgrade head`) automatically.**
5. Starts the FastAPI application server at `http://localhost:8000`.

*Access the Swagger API documentation directly at [http://localhost:8000/docs](http://localhost:8000/docs).*

### 3. Stop the Environment
```bash
docker compose down
```

---

## 📁 Folder Structure

```
telecom-backend/
├── app/
│   ├── api/          # route handlers (endpoints)
│   ├── core/          # config, DB session, security/auth
│   ├── models/          # SQLAlchemy DB models
│   ├── schemas/           # Pydantic request/response schemas
│   └── services/            # business logic, calls to AI service
├── alembic/           # DB migrations
├── tests/              # unit & integration tests
└── .github/
    └── workflows/       # CI config
```

**Rule of thumb — where code goes:**
| Type of code | Folder |
|---|---|
| New endpoint (`/complaints`, `/tickets`, `/auth`) | `app/api/` |
| DB table definition | `app/models/` |
| Request/response validation shape | `app/schemas/` |
| Business logic (e.g. "prioritize complaint", "call AI service") | `app/services/` |
| Config, env var loading, DB session, JWT/auth setup | `app/core/` |
| New DB schema change | generate via `alembic revision`, goes in `alembic/versions/` |
| Test for an endpoint/service | `tests/` (mirror the source path) |

---

## Branching Strategy

```
main        → production-ready, protected, deploy-only
  └── dev   → integration branch, all features merge here first
       ├── feature/<yourname>-<short-feature-desc>
       ├── fix/<yourname>-<short-bug-desc>-<issue-number>
       └── chore/<yourname>-<short-task-desc>
```

| Type | Format | Example |
|---|---|---|
| New feature | `feature/<name>-<feature>` | `feature/karthik-complaint-crud` |
| Bug fix | `fix/<name>-<feature>-<issue-number>` | `fix/riya-jwt-expiry-14` |
| Refactor / cleanup | `chore/<name>-<task>` | `chore/karthik-alembic-cleanup` |
| Hotfix (urgent, off main) | `hotfix/<name>-<issue>` | `hotfix/riya-prod-500` |

**Rules:**
- Never commit directly to `main` or `dev` — always via Pull Request.
- Branch off `dev`, not `main`.
- One branch = one feature/fix.
- **Do not delete branches after merge** — this is a hackathon; the full branch history is part of showcasing individual contribution. Merge via PR, keep the branch.

---

## 💻 Python Local Development Commands (Optional)

If you still wish to run or debug the server locally on your host machine using `uv`:

### 🛠️ Installing `uv`
- **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Or via Homebrew:
  brew install uv
  ```
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 🚀 Setup & Execution
```bash
# create virtual environment and install dependencies
uv sync

# run local dev server
uv run uvicorn app.main:app --reload

# run DB migrations
uv run alembic upgrade head

# create a new migration after model changes
uv run alembic revision --autogenerate -m "describe the change"

# lint check code style
uv run ruff check app/
uv run ruff format app/

# run tests
uv run pytest
```

---

## Before You Push

- [ ] Lint & Format checks pass (`uv run ruff check app/` & `uv run ruff format app/`)
- [ ] No `print()` / debug leftovers
- [ ] No secrets, API keys, DB passwords hardcoded or committed — everything through `.env`
- [ ] `.env.example` updated if you added a new required env var
- [ ] Branch up to date with latest `dev` — resolve conflicts locally

---

## Commit Message Convention

Format: `<type>: <short description>` — one line, present tense, no trailing period.
```
feat: add complaint priority endpoint
fix: resolve JWT expiry not refreshing (#14)
chore: clean up unused alembic revisions
refactor: move classification call into services layer
docs: update README setup steps
```
