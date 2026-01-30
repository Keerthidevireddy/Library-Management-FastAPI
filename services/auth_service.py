from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from app.repositories.user_repo import find_user_by_username
from app.exceptions.http_exceptions import (
    ConflictError,
    AuthenticationError
)
from app.config.settings import settings

# 🔐 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user_service(payload: dict):
    print("👉 Register payload received:", payload)

    if find_user_by_username(payload["username"]):
        raise ConflictError("User already exists")

    hashed_password = pwd_context.hash(payload["password"])

    user_doc = {
        "username": payload["username"],
        "email": payload["email"],
        "password": hashed_password,
        "organization": payload["organization"],
        "role": payload.get("role", "USER"),
        "created_at": datetime.utcnow()
    }

    from app.repositories.user_repo import create_user
    create_user(user_doc)

    print("👉 User registered successfully")
    return {"message": "User registered successfully"}


def login_user_service(payload: dict):
    print("👉 Login payload received:", payload)

    user = find_user_by_username(payload["username"])
    if not user:
        raise AuthenticationError("Invalid username or password")

    if not pwd_context.verify(payload["password"], user["password"]):
        raise AuthenticationError("Invalid username or password")

    token_payload = {
        "username": user["username"],
        "role": user["role"],
        "organization": user["organization"],
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_MINUTES)
    }

    token = jwt.encode(
        token_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    print("👉 JWT generated")
    return {"access_token": token}
