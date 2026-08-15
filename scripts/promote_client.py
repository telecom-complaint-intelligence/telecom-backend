import argparse
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set Python path to find app directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User, Profile, ServiceDetails
from app.api.auth import generate_customer_id

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/telecom_db"
)

def main():
    parser = argparse.ArgumentParser(description="Promote a user to client role in Telu database.")
    parser.add_argument("--email", required=True, help="Email of the user to promote")
    parser.add_argument("--role", default="client", help="Target role (default: client)")
    args = parser.parse_args()

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == args.email).first()
        if not user:
            print(f"User {args.email} not found in database. Creating new user...")
            user = User(
                email=args.email,
                role=args.role,
                customer_id=generate_customer_id(db),
                email_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            # Profile
            profile = Profile(
                user_id=user.id,
                name=args.email.split("@")[0].capitalize(),
                is_complete=True
            )
            db.add(profile)

            # Service details
            service = ServiceDetails(user_id=user.id)
            db.add(service)
            db.commit()
            print(f"✓ User {args.email} successfully created with role {args.role}!")
        else:
            user.role = args.role
            db.commit()
            print(f"✓ User {args.email} successfully promoted/updated to role {args.role}!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
