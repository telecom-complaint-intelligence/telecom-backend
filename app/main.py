from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router

app = FastAPI(
    title="Telecom Complaint Intelligence & Automated Resolution Assistant",
    description="FastAPI backend owning business logic, auth, database, ticket lifecycle, and AI coordination.",
    version="0.1.0",
)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Telecom Backend API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
