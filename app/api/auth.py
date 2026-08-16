import os
import random
import smtplib
import string
from datetime import UTC, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Annotated

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.redis import get_cached_data, invalidate_cache, set_cached_data
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import ClientInvitation, Department, Profile, ServiceDetails, User

load_dotenv()

router = APIRouter(prefix="/api")


# Pydantic schemas
class GoogleLoginRequest(BaseModel):
    id_token: str
    access_token: str | None = None


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileCompleteRequest(BaseModel):
    email: EmailStr
    name: str
    phone: str
    address: str
    city: str
    state_val: str
    country: str
    zipcode: str
    plan_usage: str  # "self" | "shop" | "organization"


class ServiceDetailsUpdateRequest(BaseModel):
    email: EmailStr
    account_ref: str
    bill_cycle: str
    active_plan: str
    connection_status: str
    plan_usage: str  # "self" | "shop" | "organization"


class CookieConsentRequest(BaseModel):
    email: EmailStr
    consent: bool


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOtpRequest(BaseModel):
    email: EmailStr


class VerifySessionRequest(BaseModel):
    email: EmailStr


class DepartmentCreateRequest(BaseModel):
    name: str
    requester_email: str | None = None


class DepartmentUpdateRequest(BaseModel):
    name: str
    requester_email: str


class InviteClientRequest(BaseModel):
    email: EmailStr
    password: str
    department_id: str
    requester_email: str | None = None


class OperatorUpdateRequest(BaseModel):
    department_id: str | None = None
    requester_email: str


class ActivateClientRequest(BaseModel):
    token: str


# Helper to generate unique uppercase alphanumeric customer ID
def generate_customer_id(db: Session) -> str:
    chars = string.ascii_uppercase + string.digits
    while True:
        cid = f"CUST-{''.join(random.choice(chars) for _ in range(8))}"
        exists = db.query(User).filter(User.customer_id == cid).first()
        if not exists:
            return cid


# Helper to generate 6-digit numeric OTP code
def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=6))


# Helper to send dynamic real SMTP email verification messages
def send_email_otp(to_email: str, otp: str) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    print(
        f"\n[EMAIL SYSTEM API] OTP verification code for {to_email} is: {otp} (Check your Spam folder)\n"
    )

    if not (smtp_host and smtp_port and smtp_user and smtp_pass):
        print(
            "[EMAIL SYSTEM WARNING] SMTP configuration variables not found in backend .env. Skipping real email delivery."
        )
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_from
        msg["To"] = to_email
        msg["Subject"] = f"Telu Verification Code: {otp}"

        body = f"""
        <html>
            <body style="font-family: sans-serif; padding: 25px; color: #1E0A2D; background-color: #FDFBF7;">
                <div style="max-width: 500px; margin: 0 auto; border: 1px solid #EBE6E0; padding: 20px; background-color: #ffffff; border-radius: 8px;">
                    <h2 style="font-family: serif; color: #1E0A2D; border-bottom: 1px solid #EBE6E0; padding-bottom: 10px;">Verify Your Email Address</h2>
                    <p>Hello,</p>
                    <p>Thank you for signing up with Telu. Use the 6-digit OTP verification code below to verify your email address:</p>
                    <div style="font-size: 28px; font-weight: bold; letter-spacing: 6px; padding: 15px 25px; background-color: #F3F0FF; display: inline-block; border-radius: 6px; color: #6C5CE7; margin: 20px 0; font-family: monospace;">
                        {otp}
                    </div>
                    <p style="font-size: 12px; color: #8B7E74;">This verification code is valid for 10 minutes. If you did not request this account registration, please ignore this email safety notice.</p>
                    <div style="border-top: 1px solid #EBE6E0; margin-top: 20px; padding-top: 15px; font-size: 11px; color: #8B7E74; text-align: center;">
                        © {datetime.now(UTC).year} Telu Technologies Inc. All rights reserved.
                    </div>
                </div>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        # Dispatch SMTP message
        server = smtplib.SMTP(smtp_host, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_from, to_email, msg.as_string())
        server.close()
        print(
            f"[EMAIL SYSTEM SUCCESS] Real verification email successfully sent to {to_email}"
        )
        return True
    except Exception as e:  # noqa: BLE001
        print(f"[EMAIL SYSTEM ERROR] Failed to send real SMTP email: {e}")
        return False


def send_email_invitation(to_email: str, short_link: str, department_name: str) -> bool:
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    print(
        f"\n[INVITATION SYSTEM] Activation link for {to_email} ({department_name}): {short_link}\n"
    )

    if not (smtp_host and smtp_port and smtp_user and smtp_pass):
        print(
            "[EMAIL SYSTEM WARNING] SMTP configuration variables not found. Skipping real invitation email."
        )
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_from
        msg["To"] = to_email
        msg["Subject"] = f"Invitation to join Telu Operations ({department_name})"

        body = f"""
        <html>
            <body style="font-family: sans-serif; padding: 25px; color: #1E0A2D; background-color: #FDFBF7;">
                <div style="max-width: 550px; margin: 0 auto; border: 1px solid #EBE6E0; padding: 20px; background-color: #ffffff; border-radius: 8px;">
                    <h2 style="font-family: serif; color: #1E0A2D; border-bottom: 1px solid #EBE6E0; padding-bottom: 10px;">You are Invited to Telu Operations</h2>
                    <p>Hello,</p>
                    <p>A master client has invited you to join the <strong>{department_name}</strong> operations division at Telu.</p>
                    <p>Click the link below to activate your account and complete registration:</p>
                    <div style="margin: 25px 0;">
                        <a href="{short_link}" style="background-color: #6C5CE7; color: white; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 6px; display: inline-block;">Activate Account</a>
                    </div>
                    <p style="font-size: 12px; color: #8B7E74;">If the button above does not work, copy and paste this link in your browser:</p>
                    <p style="font-size: 12px; color: #6C5CE7; font-family: monospace; word-break: break-all;">{short_link}</p>
                    <div style="border-top: 1px solid #EBE6E0; margin-top: 25px; padding-top: 15px; font-size: 11px; color: #8B7E74; text-align: center;">
                        © {datetime.now(UTC).year} Telu Technologies Inc. All rights reserved.
                    </div>
                </div>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(smtp_host, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_from, to_email, msg.as_string())
        server.close()
        return True
    except Exception as e:  # noqa: BLE001
        print(f"[INVITATION SYSTEM ERROR] Failed to send invitation email: {e}")
        return False


# Helper to build the response user object
def build_user_response(db_user: User):
    # Ensure profile and service details objects exist
    profile_data = {
        "name": None,
        "phone": None,
        "profilePicture": None,
        "address": None,
        "city": None,
        "stateVal": None,
        "country": "India",
        "zipcode": None,
    }
    service_data = {
        "accountRef": None,
        "billCycle": None,
        "activePlan": None,
        "connectionStatus": None,
        "planUsage": None,
    }

    if db_user.profile:
        profile_data = {
            "name": db_user.profile.name,
            "phone": db_user.profile.phone,
            "profilePicture": db_user.profile.profile_picture,
            "address": db_user.profile.address,
            "city": db_user.profile.city,
            "stateVal": db_user.profile.state_val,
            "country": db_user.profile.country or "India",
            "zipcode": db_user.profile.zipcode,
        }
    if db_user.service_details:
        service_data = {
            "accountRef": db_user.service_details.account_ref,
            "billCycle": db_user.service_details.bill_cycle,
            "activePlan": db_user.service_details.active_plan,
            "connectionStatus": db_user.service_details.connection_status,
            "planUsage": db_user.service_details.plan_usage,
        }

    return {
        "id": db_user.customer_id,
        "email": db_user.email,
        "role": db_user.role,
        "department": db_user.department.name if db_user.department else None,
        "isProfileComplete": db_user.profile.is_complete if db_user.profile else False,
        "emailVerified": db_user.email_verified,
        "cookieConsent": db_user.cookie_consent,
        "createdAt": db_user.created_at.isoformat() if db_user.created_at else None,
        **profile_data,
        **service_data,
    }


# 1. Google OAuth Authentication Endpoint
@router.post("/auth/google")
async def google_login(
    request: GoogleLoginRequest, db: Annotated[Session, Depends(get_db)]
):
    email = None
    name = "Telu User"
    profile_pic = None

    if request.access_token:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers={"Authorization": f"Bearer {request.access_token}"},
                    timeout=5.0,
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to Google OAuth validation server: {e!s}",
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google OAuth Access Token.",
                )

            token_info = response.json()
            email = token_info.get("email")
            name = token_info.get("name", "Telu User")
            profile_pic = token_info.get("picture")
    else:
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not google_client_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google Client ID is not configured on the server.",
            )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={request.id_token}",
                    timeout=5.0,
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to connect to Google OAuth validation server: {e!s}",
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google ID token signature or expired token.",
                )

            token_info = response.json()
            aud = token_info.get("aud")
            if aud != google_client_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token audience mismatch.",
                )

            email = token_info.get("email")
            name = token_info.get("name", "Telu User")
            profile_pic = token_info.get("picture")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account did not return a valid email address.",
        )

    # Check if user already exists in the database
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        # Check if there is an activated client invitation
        invitation = (
            db.query(ClientInvitation)
            .filter(
                ClientInvitation.email == email, ClientInvitation.is_activated == True
            )
            .first()
        )
        if invitation:
            db_user = User(
                email=email,
                role="client",
                department_id=invitation.department_id,
                customer_id=generate_customer_id(db),
                email_verified=True,
            )
        elif email == "vaahee21@gmail.com":
            db_user = User(
                email=email,
                role="client",
                customer_id=generate_customer_id(db),
                email_verified=True,
            )
        else:
            db_user = User(
                email=email,
                role="customer",
                customer_id=generate_customer_id(db),
                email_verified=True,
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create linked profile record
        db_profile = Profile(
            user_id=db_user.id,
            name=name,
            profile_picture=profile_pic,
            is_complete=False,
        )
        db.add(db_profile)

        # Create linked service details record
        db_service = ServiceDetails(user_id=db_user.id)
        db.add(db_service)
        db.commit()
        db.refresh(db_user)
    else:
        # Update user profile picture and name
        if db_user.profile:
            if profile_pic:
                db_user.profile.profile_picture = profile_pic
            if name and name != "Telu User":
                db_user.profile.name = name
            db.commit()

    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {
        "status": "success",
        "token": access_token,
        "user": build_user_response(db_user),
    }


# 2. Standard Credentials Sign-Up Endpoint
@router.post("/auth/register")
async def register_user(
    request: UserRegisterRequest, db: Annotated[Session, Depends(get_db)]
):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user account with this email address already exists.",
        )

    # Create User
    hashed = get_password_hash(request.password)
    otp = generate_otp()
    new_user = User(
        email=request.email,
        hashed_password=hashed,
        role="customer",
        customer_id=generate_customer_id(db),
        email_verified=False,
        verification_otp=otp,
        otp_created_at=datetime.now(UTC).replace(tzinfo=None),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create empty profile & service details records
    db_profile = Profile(user_id=new_user.id, is_complete=False)
    db_service = ServiceDetails(user_id=new_user.id)
    db.add(db_profile)
    db.add(db_service)
    db.commit()
    db.refresh(new_user)

    # Send verification email/OTP
    send_email_otp(new_user.email, otp)

    access_token = create_access_token(
        data={"sub": new_user.email, "role": new_user.role}
    )

    return {
        "status": "success",
        "token": access_token,
        "user": build_user_response(new_user),
    }


# 3. Standard Credentials Login Endpoint
@router.post("/auth/login")
async def login_user(
    request: UserLoginRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user or not db_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(request.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}
    )

    return {
        "status": "success",
        "token": access_token,
        "user": build_user_response(db_user),
    }


# 4. Onboarding Profile Setup Endpoint
@router.post("/auth/complete-profile")
async def complete_profile(
    request: ProfileCompleteRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found."
        )

    if not db_user.profile:
        db_user.profile = Profile(user_id=db_user.id)

    db_user.profile.name = request.name
    db_user.profile.phone = request.phone
    db_user.profile.address = request.address
    db_user.profile.city = request.city
    db_user.profile.state_val = request.state_val
    db_user.profile.country = request.country
    db_user.profile.zipcode = request.zipcode
    db_user.profile.is_complete = True

    if not db_user.service_details:
        db_user.service_details = ServiceDetails(user_id=db_user.id)
    db_user.service_details.plan_usage = request.plan_usage

    db.commit()
    db.refresh(db_user)

    return {"status": "success", "user": build_user_response(db_user)}


# 5. Service Details Update Endpoint
@router.post("/auth/service-details")
async def update_service_details(
    request: ServiceDetailsUpdateRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found."
        )

    if not db_user.service_details:
        db_user.service_details = ServiceDetails(user_id=db_user.id)

    db_user.service_details.account_ref = request.account_ref
    db_user.service_details.bill_cycle = request.bill_cycle
    db_user.service_details.active_plan = request.active_plan
    db_user.service_details.connection_status = request.connection_status
    db_user.service_details.plan_usage = request.plan_usage

    db.commit()
    db.refresh(db_user)

    return {"status": "success", "user": build_user_response(db_user)}


# 6. Cookie Consent Endpoint
@router.post("/auth/cookie-consent")
async def cookie_consent(
    request: CookieConsentRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found."
        )

    db_user.cookie_consent = request.consent
    db.commit()
    db.refresh(db_user)

    return {"status": "success", "user": build_user_response(db_user)}


# 7. Verify OTP Endpoint
@router.post("/auth/verify-otp")
async def verify_otp(
    request: VerifyOtpRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found."
        )

    if not db_user.verification_otp or db_user.verification_otp != request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 6-digit verification code.",
        )

    if db_user.otp_created_at:
        diff = datetime.now(UTC).replace(tzinfo=None) - db_user.otp_created_at
        if diff.total_seconds() > 600:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired. Please request a new one.",
            )

    db_user.email_verified = True
    db_user.verification_otp = None
    db_user.otp_created_at = None
    db.commit()
    db.refresh(db_user)

    return {"status": "success", "user": build_user_response(db_user)}


# 8. Resend OTP Endpoint
@router.post("/auth/resend-otp")
async def resend_otp(
    request: ResendOtpRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User account not found."
        )

    otp = generate_otp()
    db_user.verification_otp = otp
    db_user.otp_created_at = datetime.now(UTC).replace(tzinfo=None)
    db.commit()

    # Send verification email/OTP
    send_email_otp(db_user.email, otp)

    return {
        "status": "success",
        "message": "OTP verification code resent successfully.",
    }


# 9. Verify Session Endpoint
@router.post("/auth/verify-session")
async def verify_session(
    request: VerifySessionRequest, db: Annotated[Session, Depends(get_db)]
):
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User session is invalid or deleted.",
        )
    return {"status": "success", "user": build_user_response(db_user)}


# 10. List Departments
@router.get("/auth/departments")
async def get_departments(db: Annotated[Session, Depends(get_db)]):
    cache_key = "telu:departments"
    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    departments = db.query(Department).filter(Department.is_archived == False).all()
    result = [{"id": d.id, "name": d.name} for d in departments]
    set_cached_data(cache_key, result, expire_seconds=300)
    return result


# 11. Create Department
@router.post("/auth/departments")
async def create_department(
    request: DepartmentCreateRequest, db: Annotated[Session, Depends(get_db)]
):
    if request.requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )

    # Check if department already exists
    existing = (
        db.query(Department)
        .filter(Department.name == request.name, Department.is_archived == False)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department already exists.",
        )

    dept = Department(name=request.name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    invalidate_cache("telu:departments")
    return {"status": "success", "department": {"id": dept.id, "name": dept.name}}


# 12. Invite Client
@router.post("/auth/invite-client")
async def invite_client(
    request: InviteClientRequest, db: Annotated[Session, Depends(get_db)]
):
    if request.requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )

    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter(User.email == request.email, User.is_archived == False)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    # Check if department exists
    dept = (
        db.query(Department)
        .filter(Department.id == request.department_id, Department.is_archived == False)
        .first()
    )
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified department not found.",
        )

    # Check if invitation already exists
    existing_invite = (
        db.query(ClientInvitation)
        .filter(ClientInvitation.email == request.email)
        .first()
    )
    if existing_invite:
        db.delete(existing_invite)
        db.commit()

    import uuid

    token = str(uuid.uuid4())
    expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=7)

    hashed_pass = get_password_hash(request.password)

    invitation = ClientInvitation(
        email=request.email,
        department_id=request.department_id,
        token=token,
        hashed_password=hashed_pass,
        expires_at=expires_at,
    )
    db.add(invitation)
    db.commit()
    invalidate_cache("telu:operators:*")
    db.refresh(invitation)

    # Build shortened link pointing to backend redirection route
    backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    short_link = f"{backend_url}/api/auth/lnk/{token}"

    # Send SMTP invitation email
    send_email_invitation(request.email, short_link, dept.name)

    return {
        "status": "success",
        "message": f"Invitation successfully sent to {request.email}.",
    }


# 13. Activate Invitation
@router.post("/auth/activate-client")
async def activate_client(
    request: ActivateClientRequest, db: Annotated[Session, Depends(get_db)]
):
    invitation = (
        db.query(ClientInvitation)
        .filter(ClientInvitation.token == request.token)
        .first()
    )
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation token is invalid or does not exist.",
        )

    if invitation.expires_at < datetime.now(UTC).replace(tzinfo=None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation token has expired.",
        )

    if invitation.is_activated:
        return {"status": "success", "message": "Account has already been activated."}

    # Toggle activated flag
    invitation.is_activated = True
    db.commit()

    # Provision user record
    db_user = db.query(User).filter(User.email == invitation.email).first()
    if not db_user:
        db_user = User(
            email=invitation.email,
            hashed_password=invitation.hashed_password,
            role="client",
            department_id=invitation.department_id,
            customer_id=generate_customer_id(db),
            email_verified=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create linked profile record
        db_profile = Profile(
            user_id=db_user.id,
            name=invitation.email.split("@")[0].capitalize(),
            is_complete=True,
        )
        db.add(db_profile)

        # Create linked service details record
        db_service = ServiceDetails(user_id=db_user.id)
        db.add(db_service)
        db.commit()
        db.refresh(db_user)

    return {
        "status": "success",
        "message": "Account activated successfully. Please sign in.",
    }


# 14. Resolve Short Link Redirect
@router.get("/auth/lnk/{token}")
async def resolve_short_link(token: str, db: Annotated[Session, Depends(get_db)]):
    invitation = (
        db.query(ClientInvitation).filter(ClientInvitation.token == token).first()
    )
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link is invalid or has expired.",
        )

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return RedirectResponse(url=f"{frontend_url}/auth/activate?token={token}")


# 15. Get Operators/Client Staff List
@router.get("/auth/operators")
async def get_operators(email: str, db: Annotated[Session, Depends(get_db)]):
    if not email:
        return []

    cache_key = f"telu:operators:{email}"
    cached = get_cached_data(cache_key)
    if cached is not None:
        return cached

    current_user = db.query(User).filter(User.email == email).first()
    if not current_user:
        return []

    operators = (
        db.query(User).filter(User.role == "client", User.is_archived == False).all()
    )
    is_master_admin = current_user.email == "vaahee21@gmail.com"

    result = []
    for op in operators:
        # If not the master admin, restrict visibility to the same department
        if (
            not is_master_admin
            and current_user
            and current_user.department_id != op.department_id
        ):
            continue

        name = op.profile.name if op.profile else op.email.split("@")[0].capitalize()
        dept_name = op.department.name if op.department else "Unmapped"
        result.append(
            {
                "id": op.customer_id,
                "name": name,
                "email": op.email,
                "department": dept_name,
                "status": "Active" if op.email_verified else "Pending",
            }
        )

    set_cached_data(cache_key, result, expire_seconds=300)
    return result


# 16. Update Department Name
@router.put("/auth/departments/{id}")
async def update_department(
    id: str, request: DepartmentUpdateRequest, db: Annotated[Session, Depends(get_db)]
):
    if request.requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )
    dept = (
        db.query(Department)
        .filter(Department.id == id, Department.is_archived == False)
        .first()
    )
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found.",
        )

    dept.name = request.name
    db.commit()
    invalidate_cache("telu:departments")
    invalidate_cache("telu:operators:*")
    return {"status": "success"}


# 17. Archive/Soft-delete Department
@router.delete("/auth/departments/{id}")
async def archive_department(
    id: str, requester_email: str, db: Annotated[Session, Depends(get_db)]
):
    if requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )
    dept = (
        db.query(Department)
        .filter(Department.id == id, Department.is_archived == False)
        .first()
    )
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found.",
        )

    dept.is_archived = True
    db.commit()
    invalidate_cache("telu:departments")
    invalidate_cache("telu:operators:*")
    return {"status": "success"}


# 18. Update Operator Department Mapping
@router.put("/auth/operators/{id}")
async def update_operator(
    id: str, request: OperatorUpdateRequest, db: Annotated[Session, Depends(get_db)]
):
    if request.requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )
    op = (
        db.query(User).filter(User.customer_id == id, User.is_archived == False).first()
    )
    if not op:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )

    op.department_id = request.department_id
    db.commit()
    invalidate_cache("telu:operators:*")
    return {"status": "success"}


# 19. Archive/Soft-delete Operator
@router.delete("/auth/operators/{id}")
async def archive_operator(
    id: str, requester_email: str, db: Annotated[Session, Depends(get_db)]
):
    if requester_email != "vaahee21@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the Master Client Admin can perform this action.",
        )
    op = (
        db.query(User).filter(User.customer_id == id, User.is_archived == False).first()
    )
    if not op:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )

    op.is_archived = True
    db.commit()
    invalidate_cache("telu:operators:*")
    return {"status": "success"}
