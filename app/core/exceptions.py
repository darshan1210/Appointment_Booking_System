"""Custom exceptions for the application."""


class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(AppException):
    """Authentication related errors."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(AppException):
    """Authorization/permission errors."""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, status_code=403)


class NotFoundError(AppException):
    """Resource not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ConflictError(AppException):
    """Resource conflict."""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status_code=409)


class ValidationError(AppException):
    """Validation error."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)
