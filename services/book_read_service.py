from app.config.database import db
from app.utils.pagination import paginate
from app.exceptions.http_exceptions import AuthorizationError

books_col = db["books"]


def serialize_book(book):
    """Convert MongoDB document to JSON-serializable dict."""
    if book and "_id" in book:
        book["_id"] = str(book["_id"])
    return book


def list_books_service(user, status=None, page=1, size=10, admin_view=False):
    skip, limit = paginate(page, size)

    query = {"is_deprecated": False}

    # Default search 
    if not status:
        if user["role"] == "ADMIN" and admin_view:
            pass
        else:
            query["$or"] = [
                {"status": "PUBLISHED"},
                {"created_by": user["username"]}
            ]
    else:
        query["status"] = status

    # Visibility rules
    if status == "DRAFT":
        if user["role"] != "ADMIN":
            query["created_by"] = user["username"]

    if status == "REJECTED":
        if user["role"] != "ADMIN":
            query["created_by"] = user["username"]

    if status in ["ARCHIVED", "DEPRECATED"] and not admin_view:
        raise AuthorizationError("Admin access required")

    books = list(
        books_col.find(query)
        .sort([("created_at", -1), ("last_modified", -1)])
        .skip(skip)
        .limit(limit)
    )

    # Serialize ObjectIds to strings
    books = [serialize_book(book) for book in books]

    total = books_col.count_documents(query)

    return {
        "page": page,
        "size": size,
        "total": total,
        "data": books
    }
