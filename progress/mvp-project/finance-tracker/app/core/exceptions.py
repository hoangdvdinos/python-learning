class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: int | str) -> None:
        super().__init__(
            message=f"{resource} with id={resource_id} not found",
            status_code=404,
        )


class BusinessException(AppException):
    """Raised when a business rule is violated."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=400)
