class BookException(Exception):
    pass

class BookAlreadyExists(BookException):
    pass

class UnauthorizedBookAction(BookException):
    pass

class InvalidStatusChange(BookException):
    pass
