from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    def __init__(self, message="Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class AuthorizationError(HTTPException):
    def __init__(self, message="Not authorized"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class ResourceNotFoundError(HTTPException):
    def __init__(self, message="Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )


class ConflictError(HTTPException):
    def __init__(self, message="Conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class ValidationError(HTTPException):
    def __init__(self, message="Validation error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
