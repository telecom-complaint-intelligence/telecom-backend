import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5433/telecom_db"
)


def create_db_engine():
    if DATABASE_URL.startswith("sqlite"):
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    try:
        pg_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with pg_engine.connect():
            pass
        return pg_engine
    except Exception as e:  # noqa: BLE001
        print(f"Notice: PostgreSQL connection ({e}). Using local SQLite database.")
        sqlite_url = "sqlite:///./telecom_backend.db"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
