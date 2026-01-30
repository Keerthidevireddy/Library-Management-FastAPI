from fastapi import APIRouter, Depends, status

from app.models.book_models import (
    BookCreateRequest,
    BookPatchRequest,
    BookStatusUpdateRequest
)
from app.services.book_service import (
    create_book_service,
    update_book_service,
    change_status_service,
    delete_book_service
)
from app.utils.role_guard import require_roles

router = APIRouter(prefix="/books", tags=["Books"])


# =====================================================
# CREATE BOOK
# AUTHOR + ADMIN
# =====================================================
@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(
    req: BookCreateRequest,
    user=Depends(require_roles("AUTHOR", "ADMIN"))
):
    return create_book_service(req.dict(), user)


# =====================================================
# UPDATE BOOK (PATCH)
# AUTHOR + ADMIN
# =====================================================
@router.patch("/{book_id}", status_code=status.HTTP_200_OK)
def update_book(
    book_id: str,
    req: BookPatchRequest,
    user=Depends(require_roles("AUTHOR", "ADMIN"))
):
    return update_book_service(
        book_id,
        req.dict(exclude_none=True),
        user
    )


# =====================================================
# UPDATE BOOK STATUS
# ADMIN ONLY
# =====================================================
@router.patch("/{book_id}/status", status_code=status.HTTP_200_OK)
def update_status(
    book_id: str,
    req: BookStatusUpdateRequest,
    user=Depends(require_roles("ADMIN"))
):
    return change_status_service(
        book_id,
        req.dict(),
        user
    )


# =====================================================
# SOFT DELETE BOOK
# ADMIN ONLY
# =====================================================
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: str,
    user=Depends(require_roles("ADMIN"))
):
    delete_book_service(book_id, user)
    return None
