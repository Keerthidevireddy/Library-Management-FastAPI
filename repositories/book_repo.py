from app.config.database import db
from bson import ObjectId
from bson.errors import InvalidId
from app.exceptions.http_exceptions import ValidationError, ConflictError

books_col = db["books"]


def to_object_id(book_id: str) -> ObjectId:
    """Convert string to ObjectId with validation."""
    try:
        return ObjectId(book_id)
    except InvalidId:
        raise ValidationError(f"Invalid book ID format: {book_id}")


def find_book_by_title(title: str):
    return books_col.find_one(
        {"title": title, "is_deprecated": False}
    )


def find_book_by_id(book_id: str):
    return books_col.find_one({"_id": to_object_id(book_id)})


def insert_books_bulk(book_docs: list):
    books_col.insert_many(book_docs)


def update_book_atomic(book_id: str, update_data: dict, version: int, history_entry: dict | None = None):
    update_ops = {
        "$set": update_data,
        "$inc": {"version": 1}
    }
    if history_entry:
        update_ops["$push"] = {"history": history_entry}

    result = books_col.update_one(
        {"_id": to_object_id(book_id), "version": version},
        update_ops
    )
    if result.matched_count == 0:
        raise ConflictError("Concurrent update detected - version mismatch")


def soft_delete_book(book_id: str, history_entry: dict | None = None):
    update_ops = {"$set": {"is_deprecated": True}}
    if history_entry:
        update_ops["$push"] = {"history": history_entry}

    books_col.update_one(
        {"_id": to_object_id(book_id)},
        update_ops
    )
