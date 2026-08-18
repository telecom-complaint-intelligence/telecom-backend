# =============================================================================
# Telecom Backend — Production Dockerfile
# FastAPI + uv | Python 3.11 Slim | Alembic Migrations
# =============================================================================

# Stage 1: Dependency resolution & build
FROM python:3.11-slim AS builder

# Install uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy lock files first for Docker layer caching
COPY pyproject.toml uv.lock ./

# Install production dependencies only (no dev)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application source
COPY app ./app

# Install the project itself into the venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# =============================================================================
# Stage 2: Minimal production runtime
# =============================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Create non-root user for security
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --no-create-home appuser

# Copy virtual environment and app artifacts from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app ./app

# Copy Alembic migrations and startup script
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY start.sh ./start.sh

RUN chmod +x ./start.sh

# Use the virtualenv binaries
ENV PATH="/app/.venv/bin:$PATH"

# Runtime environment defaults (override via --env-file or cloud secret injection)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()" || exit 1

CMD ["./start.sh"]
