from fastapi.responses import JSONResponse
from app.exceptions.book_exceptions import (
    UnauthorizedBookAction,
    InvalidStatusChange,
    BookAlreadyExists
)


def book_exception_handler(request, exc):
    status_code = 400

    if isinstance(exc, UnauthorizedBookAction):
        status_code = 403
    elif isinstance(exc, InvalidStatusChange):
        status_code = 409
    elif isinstance(exc, BookAlreadyExists):
        status_code = 409

    return JSONResponse(
        status_code=status_code,
        content={
            "error": str(exc),
            "path": request.url.path
        }
    )
