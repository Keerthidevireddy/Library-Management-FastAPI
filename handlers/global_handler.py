from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback

def http_exception_handler(request: Request, exc: HTTPException):
    print("🔥 HTTP EXCEPTION:", exc.detail)
    traceback.print_exc()

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
            "path": request.url.path
        }
    )
