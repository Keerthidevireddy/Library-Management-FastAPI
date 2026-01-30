from datetime import datetime

from app.repositories.book_repo import (
    find_book_by_title,
    find_book_by_id,
    insert_books_bulk,
    update_book_atomic,
    soft_delete_book
)
from app.services.book_fsm import validate_fsm_transition

from app.utils.book_validators import (
    validate_inventory,
    validate_publication_year,
    validate_non_empty_draft
)

from app.exceptions.book_exceptions import UnauthorizedBookAction
from app.exceptions.http_exceptions import (
    ConflictError,
    ResourceNotFoundError
)

# =====================================================
# CREATE BOOK
# =====================================================

def _build_history_entry(change_type: str, user: dict, summary: str, changes: list, catalog_version: int):
    return {
        "catalog_version": str(catalog_version),
        "changed_on": datetime.utcnow(),
        "changed_by": user["username"],
        "change_type": change_type,
        "summary": summary,
        "changes": changes
    }


def create_book_service(payload: dict, user: dict):
    # Duplicate book check
    if find_book_by_title(payload["title"]):
        raise ConflictError("Book already exists")

    # Validations
    validate_inventory(
        payload["total_copies"],
        payload["available_copies"],
        payload["reserved_copies"]
    )
    validate_publication_year(payload["publication_year"])

    history_entry = _build_history_entry(
        change_type="CREATE",
        user=user,
        summary="Book created",
        changes=[
            {"path": key, "old_value": None, "new_value": value}
            for key, value in payload.items()
        ],
        catalog_version=1
    )

    book_doc = {
        **payload,
        "status": "DRAFT",
        "created_by": user["username"],
        "organization": user["organization"],
        "created_at": datetime.utcnow(),
        "last_modified": datetime.utcnow(),
        "last_modified_person_name": user["username"],
        "version": 1,
        "is_archived": False,
        "is_deprecated": False,
        "admin_action_taken": False,
        "approved_by": None,
        "rejection_reason": None,
        "history": [history_entry]
    }

    insert_books_bulk([book_doc])

    # Convert for JSON serialization
    book_doc["last_modified"] = book_doc["last_modified"].isoformat()
    if "_id" in book_doc:
        book_doc["_id"] = str(book_doc["_id"])
    return book_doc


# =====================================================
# UPDATE BOOK (PATCH)
# =====================================================

def update_book_service(book_id: str, payload: dict, user: dict):
    # 1️⃣ Fetch book
    book = find_book_by_id(book_id)
    if not book:
        raise ResourceNotFoundError("Book not found")

    # 2️⃣ Ownership / Admin check
    if book["created_by"] != user["username"] and user["role"] != "ADMIN":
        raise UnauthorizedBookAction("You cannot modify this book")

    # 3️⃣ STRICT FIELD LOCK — title
    if book["status"] in ["APPROVED", "PUBLISHED"] and "title" in payload:
        raise ConflictError("Title cannot be modified after approval")

    # 4️⃣ Approved / Published → metadata edit resets to DRAFT
    if book["status"] in ["APPROVED", "PUBLISHED"]:
        payload["status"] = "DRAFT"
        payload["admin_action_taken"] = False
        payload["approved_by"] = None

    # 5️⃣ Update atomically with optimistic locking
    changes = []
    for key, new_value in payload.items():
        old_value = book.get(key)
        if old_value != new_value:
            changes.append(
                {"path": key, "old_value": old_value, "new_value": new_value}
            )

    summary = "Updated fields: " + ", ".join([c["path"] for c in changes]) if changes else "No field changes"
    history_entry = _build_history_entry(
        change_type="UPDATE",
        user=user,
        summary=summary,
        changes=changes,
        catalog_version=book["version"] + 1
    )

    update_book_atomic(
        book_id,
        {
            **payload,
            "last_modified": datetime.utcnow(),
            "last_modified_person_name": user["username"]
        },
        book["version"],
        history_entry=history_entry
    )

    return {"message": "Book updated successfully"}


# =====================================================
# CHANGE BOOK STATUS (ADMIN ONLY)
# =====================================================

def change_status_service(book_id: str, payload: dict, user: dict):
    # 1️⃣ Fetch book
    book = find_book_by_id(book_id)
    if not book:
        raise ResourceNotFoundError("Book not found")

    # 2️⃣ Role enforcement
    if user["role"] != "ADMIN":
        raise UnauthorizedBookAction("Only admin can change book status")

    # 3️⃣ ADMIN ACTION IMMUTABILITY
    if book.get("admin_action_taken") is True:
        raise ConflictError("Admin action is immutable and cannot be changed")

    # 4️⃣ FSM validation
    validate_fsm_transition(book["status"], payload["target_status"])

    # 5️⃣ Draft validation before approval request
    if payload["target_status"] == "REQUESTED_FOR_APPROVAL":
        validate_non_empty_draft(book)

    # 6️⃣ STRICT REJECTION REASON (REQUIREMENT #8)
    if payload["target_status"] == "REJECTED":
        if not payload.get("rejection_reason") or not payload["rejection_reason"].strip():
            raise ConflictError("Rejection reason is mandatory")
        
    if payload["target_status"] == "REJECTED" and not payload.get("rejection_reason"):
        raise ConflictError("Rejection reason is required when rejecting a book")

    # 7️⃣ Perform status update
    history_entry = _build_history_entry(
        change_type="STATUS_CHANGE",
        user=user,
        summary=f"Status changed from {book['status']} to {payload['target_status']}",
        changes=[
            {
                "path": "status",
                "old_value": book["status"],
                "new_value": payload["target_status"]
            },
            {
                "path": "rejection_reason",
                "old_value": book.get("rejection_reason"),
                "new_value": payload.get("rejection_reason")
            }
        ] if payload["target_status"] == "REJECTED" else [
            {
                "path": "status",
                "old_value": book["status"],
                "new_value": payload["target_status"]
            }
        ],
        catalog_version=book["version"] + 1
    )

    update_book_atomic(
        book_id,
        {
            "status": payload["target_status"],
            "rejection_reason": payload.get("rejection_reason"),
            "approved_by": user["username"],
            "admin_action_taken": True,
            "last_modified": datetime.utcnow(),
            "last_modified_person_name": user["username"]
        },
        payload["version"],
        history_entry=history_entry
    )


    return {"message": f"Book status updated to {payload['target_status']}"}


# =====================================================
# SOFT DELETE BOOK (ADMIN ONLY)
# =====================================================

def delete_book_service(book_id: str, user: dict):
    if user["role"] != "ADMIN":
        raise UnauthorizedBookAction("Only admin can delete books")

    book = find_book_by_id(book_id)
    if not book:
        raise ResourceNotFoundError("Book not found")

    history_entry = _build_history_entry(
        change_type="DELETE",
        user=user,
        summary="Book soft-deleted",
        changes=[
            {
                "path": "is_deprecated",
                "old_value": book.get("is_deprecated"),
                "new_value": True
            }
        ],
        catalog_version=book["version"]
    )

    soft_delete_book(book_id, history_entry=history_entry)
    return {"message": "Book soft-deleted successfully"}
