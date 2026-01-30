from app.exceptions.http_exceptions import ValidationError


def paginate(page: int, size: int):
    if page < 1 or size < 1:
        raise ValidationError("Invalid pagination parameters")
    skip = (page - 1) * size
    return skip, size
