"""
Server-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError


class ServerError(RecallrAIError):
    """
    Base class for server-related exceptions.
    
    This exception serves as the base for all exceptions related to
    server-side errors in the RecallrAI API.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class InternalServerError(ServerError):
    """
    Raised when the RecallrAI API encounters an internal server error.
    
    This exception is typically raised when the API returns a 5xx error code.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class RateLimitError(ServerError):
    """
    Raised when the API rate limit has been exceeded.

    This exception is raised when too many requests are made in a
    short period of time.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

# class ServiceUnavailableError(ServerError):
#     """
#     Raised when the RecallrAI service is temporarily unavailable.
#
#     This exception is raised when the API is down for maintenance
#     or experiencing issues.
#     """
#
#     def __init__(
#         self, 
#         message: str = "Service temporarily unavailable.", 
#         code: str = "service_unavailable",
#         http_status: int = 503,
#         retry_after: Optional[int] = None,
#         details: Optional[Dict[str, Any]] = None
#     ):
#         details = details or {}
#         if retry_after:
#             details["retry_after"] = retry_after
#         super().__init__(message, code, http_status, details)
#         self.retry_after = retry_after
