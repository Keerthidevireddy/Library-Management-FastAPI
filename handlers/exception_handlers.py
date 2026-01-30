from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import AuthException

def auth_exception_handler(request, exc: AuthException):
    return JSONResponse(
        status_code=401,
        content={
            "error": str(exc),
            "path": request.url.path
        }
    )
