from app.config.database import db

books_col = db["books"]

def get_dashboard_counts(user):
    base = {"is_deprecated": False}
    if user["role"] != "ADMIN":
        base["created_by"] = user["username"]

    return {
        "draft": books_col.count_documents({**base, "status": "DRAFT"}),
        "requested": books_col.count_documents({**base, "status": "REQUESTED_FOR_APPROVAL"}),
        "approved": books_col.count_documents({**base, "status": "APPROVED"}),
        "published": books_col.count_documents({**base, "status": "PUBLISHED"}),
        "rejected": books_col.count_documents({**base, "status": "REJECTED"}),
    }
