from fastapi import Depends
from app.middlewares.auth_guard import get_current_user
from app.exceptions.http_exceptions import AuthorizationError


def require_roles(*allowed_roles):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise AuthorizationError(
                f"Role '{user['role']}' not permitted"
            )
        return user
    return checker
