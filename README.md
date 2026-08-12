# telecom-backend

FastAPI backend for the Telecom Complaint Intelligence & Automated Resolution Assistant — owns business logic, auth, database, ticket lifecycle, and orchestrates calls to `telecom-ai-service` for classification, sentiment, RAG, and agentic triage.

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

Endpoints in `api/` should stay thin — validate input, call a `service`, return the response. Actual logic (talking to DB, calling AI service, computing priority) belongs in `services/`, not inline in the route handler. This keeps things testable and keeps 3 backend devs from stepping on each other inside giant route files.

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
- Keep PR descriptions detailed (what was built, how tested, linked issue) — this is what's easiest to reference/screenshot later for showcase purposes.

### Flow

```
1. git checkout dev
2. git pull origin dev
3. git checkout -b feature/<name>-<feature>
4. ... code, commit ...
5. git push origin feature/<name>-<feature>
6. Open PR: feature/<name>-<feature> → dev
7. Get 1 review approval + CI passing
8. Merge (branch stays, not deleted)
9. Periodically: dev → main (when stable, via PR)
```

---

## 💻 Commands (run from repo root: `telecom-backend/`)

### 🛠️ Installing `uv` (if not present)

You must install `uv` before setting up the project:

- **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Or via Homebrew:
  brew install uv
  ```
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  # Or via winget:
  winget install --id Astral.uv
  ```

*Restart your terminal after installation.*

### 🚀 Setup & Development

```bash
# create virtual environment and install dependencies
uv sync

# activate virtual environment (optional, uv run handles execution automatically)
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# add a dependency
uv add <package_name>

# run local dev server
uv run uvicorn app.main:app --reload     # http://localhost:8000
                                         # docs at /docs (Swagger)

# run DB migrations
uv run alembic upgrade head

# create a new migration after model changes
uv run alembic revision --autogenerate -m "describe the change"

# lint
uv run ruff check app/

# run tests
uv run pytest

# run with coverage
uv run pytest --cov=app
```

> All commands run from the **repo root**. If using Docker instead: `docker-compose up --build` runs backend + DB together — check `docker-compose.yml` for service names/ports.

---

## Before You Start Coding (after `git pull`)

- [ ] Confirm you're on the correct branch (`git branch`)
- [ ] Pulled latest `dev`: `git pull origin dev`
- [ ] `uv sync` — dependencies may have changed
- [ ] `.env` present and up to date (check `.env.example` for new variables — especially `AI_SERVICE_URL`, DB connection string)
- [ ] `alembic upgrade head` — apply any new migrations before running the app
- [ ] `uvicorn app.main:app --reload` — confirm it boots clean, hit `/docs` to sanity-check
- [ ] Check open PRs/issues board — avoid duplicate work on the same endpoint/model

---

## Before You Push

- [ ] Lint passes (`uv run ruff check app/`)
- [ ] `pytest` — all tests pass, added/updated tests for what changed
- [ ] If you changed a model, migration generated (`alembic revision --autogenerate`) and included in the commit
- [ ] No `print()` / debug leftovers
- [ ] No secrets, API keys, DB passwords hardcoded or committed — everything through `.env`
- [ ] `.env.example` updated if you added a new required env var
- [ ] Endpoint tested manually via `/docs` (Swagger) at least once
- [ ] Branch up to date with latest `dev` — resolve conflicts locally
- [ ] PR description filled: what changed, why, how tested, linked issue number

---

## Commit Message Convention

```
feat: add complaint priority endpoint
fix: resolve JWT expiry not refreshing (#14)
chore: clean up unused alembic revisions
refactor: move classification call into services layer
docs: update README setup steps
```

Format: `<type>: <short description>` — one line, present tense, no trailing period.
