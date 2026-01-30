from bson import ObjectId
from bson.errors import InvalidId
from app.config.database import db
from app.exceptions.http_exceptions import ConflictError, ValidationError

books_col = db["books"]


def bulk_inventory_update_service(payload: dict):
    if not any(
        payload.get(field) is not None
        for field in ["available_copies", "total_copies", "reserved_copies"]
    ):
        raise ConflictError("At least one inventory field must be provided")

    book_ids = payload.get("book_ids", [])
    if not book_ids:
        raise ValidationError("No book IDs provided")

    # Convert string IDs to ObjectIds
    try:
        object_ids = [ObjectId(bid) for bid in book_ids]
    except InvalidId as e:
        raise ValidationError(f"Invalid book ID format: {e}")

    # Build update document
    update_fields = {}
    if payload.get("available_copies") is not None:
        update_fields["available_copies"] = payload["available_copies"]
    if payload.get("total_copies") is not None:
        update_fields["total_copies"] = payload["total_copies"]
    if payload.get("reserved_copies") is not None:
        update_fields["reserved_copies"] = payload["reserved_copies"]

    # Perform bulk update
    result = books_col.update_many(
        {"_id": {"$in": object_ids}},
        {"$set": update_fields}
    )

    return {"modified_count": result.modified_count}
