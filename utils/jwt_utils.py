from jose import jwt
from datetime import datetime, timedelta
from app.config.settings import settings

def generate_token(payload: dict) -> str:
    payload["exp"] = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXP_MINUTES
    )
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

