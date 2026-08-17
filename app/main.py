from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ai import router as ai_router
from app.api.auth import router as auth_router
from app.api.complaints import router as complaint_router
from app.core.database import Base, engine
from app.models import complaints, user  # noqa: F401

# Initialize database tables automatically if missing
try:
    Base.metadata.create_all(bind=engine)
except (RuntimeError, ValueError, OSError) as e:
    print(f"Notice: Database table initialization note ({e})")

app = FastAPI(
    title="Telecom Complaint Intelligence & Automated Resolution Assistant",
    description="FastAPI backend owning business logic, auth, database, ticket lifecycle, and AI coordination.",
    version="0.1.0",
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)
app.include_router(complaint_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Telecom Backend API!",
        "docs": "/docs",
        "service": "telecom-backend",
        "port": 8000,
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
