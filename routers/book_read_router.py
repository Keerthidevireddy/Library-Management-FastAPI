from fastapi import APIRouter, Depends, Query
from app.services.book_read_service import list_books_service
from app.middlewares.auth_guard import get_current_user

router = APIRouter(prefix="/books", tags=["Books-Read"])


@router.get("")
def list_books(
    status: str | None = Query(None),
    page: int = Query(1),
    size: int = Query(10),
    admin_view: bool = Query(False),
    user=Depends(get_current_user)
):
    return list_books_service(
        user=user,
        status=status,
        page=page,
        size=size,
        admin_view=admin_view
    )
