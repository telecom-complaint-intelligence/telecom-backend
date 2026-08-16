import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

load_dotenv()

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "your_telu_super_secret_session_jwt_key_321"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Security Bearer for Swagger UI lock icon
security_bearer_optional = HTTPBearer(auto_error=False)
security_bearer_required = HTTPBearer(auto_error=True)


def get_password_hash(password: str) -> str:
    # Hash password using bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify password against bcrypt hash
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # Encode JWT payload with expiration claim
    to_encode = data.copy()
    now_utc = datetime.now(UTC)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Store expiration claim as timestamp
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_optional_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(security_bearer_optional)
    ] = None,
    db: Annotated[Session, Depends(get_db)] = None,
) -> User | None:
    """
    Optional dependency: Decodes JWT Bearer token if provided.
    Returns User object or None if guest/unauthenticated.
    """
    if not credentials:
        return None

    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            return None
        return db.query(User).filter(User.email == email).first()
    except (jwt.PyJWTError, ValueError):
        return None


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(security_bearer_required)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Strict dependency: Requires customer to be authenticated.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token is missing sub claim.",
            )
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User associated with token not found.",
            )
        return user
    except (jwt.PyJWTError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is invalid or expired.",
        ) from exc
