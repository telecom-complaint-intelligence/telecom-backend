import os
import sys

from sqlalchemy import text

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models to register them with SQLAlchemy Base metadata
import app.models  # noqa: F401
from app.core.database import Base, SessionLocal
from app.core.redis import redis_client


def clear_db():
    db = SessionLocal()
    try:
        # Sort tables by dependency (parent to child), and reverse it to delete children first
        reversed_tables = reversed(Base.metadata.sorted_tables)
        
        for table in reversed_tables:
            print(f"Clearing table: {table.name}")
            db.execute(text(f"DELETE FROM {table.name};"))
            
        db.commit()
        print("Database tables cleared successfully!")

        # Flush Redis cache
        if redis_client:
            try:
                redis_client.flushdb()
                print("Redis cache flushed successfully!")
            except Exception as rx:
                print(f"Warning: Could not flush Redis cache: {rx}")
    except Exception as e:
        db.rollback()
        print(f"Error clearing database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    clear_db()
