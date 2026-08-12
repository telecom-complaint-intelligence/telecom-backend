from fastapi import FastAPI

app = FastAPI(
    title="Telecom Complaint Intelligence & Automated Resolution Assistant",
    description="FastAPI backend owning business logic, auth, database, ticket lifecycle, and AI coordination.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Telecom Backend API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
