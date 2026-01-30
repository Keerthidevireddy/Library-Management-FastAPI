from datetime import datetime
from app.exceptions.http_exceptions import ValidationError


def validate_inventory(total, available, reserved):
    if total < (available + reserved):
        raise ValidationError("Total copies must be >= available + reserved")


def validate_publication_year(year):
    if year > datetime.utcnow().year:
        raise ValidationError("Publication year cannot be in the future")


def validate_non_empty_draft(book):
    mandatory_fields = ["title", "author", "category"]
    for field in mandatory_fields:
        if not book.get(field):
            raise ValidationError("Draft is incomplete and cannot be submitted")
