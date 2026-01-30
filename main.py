from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.book_router import router as book_router
from app.routers.book_read_router import router as book_read_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.bulk_router import router as bulk_router
from app.routers.role_router import router as role_router

from app.exceptions.book_exceptions import BookException
from app.handlers.book_exception_handlers import book_exception_handler

app = FastAPI(title="Library Management API")

# Register exception handlers
app.add_exception_handler(BookException, book_exception_handler)

# Include routers
app.include_router(auth_router)
app.include_router(book_router)
app.include_router(book_read_router)
app.include_router(dashboard_router)
app.include_router(bulk_router)
app.include_router(role_router)


