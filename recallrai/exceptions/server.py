"""
Server-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .base import RecallrAIError


class ServerError(RecallrAIError):
    """
    Base class for server-related exceptions.
    """
    def __init__(
        self, 
        message: str = "Server error occurred", 
        code: str = "server_error",
        http_status: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)

class InternalServerError(ServerError):
    """
    Raised when the RecallrAI API encounters an internal server error.
    
    This exception is typically raised when the API returns a 5xx error code.
    """

    def __init__(
        self, 
        message: str = "Internal server error", 
        code: str = "server_error",
        http_status: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)


# class RateLimitError(ServerError):
#     """
#     Raised when the API rate limit has been exceeded.
#
#     This exception is raised when too many requests are made in a
#     short period of time.
#     """

#     def __init__(
#         self, 
#         message: str = "API rate limit exceeded", 
#         code: str = "rate_limit_exceeded",
#         http_status: int = 429,
#         retry_after: Optional[int] = None,
#         details: Optional[Dict[str, Any]] = None
#     ):
#         details = details or {}
#         if retry_after:
#             details["retry_after"] = retry_after
#         super().__init__(message, code, http_status, details)
#         self.retry_after = retry_after


# class ServiceUnavailableError(ServerError):
#     """
#     Raised when the RecallrAI service is temporarily unavailable.
#
#     This exception is raised when the API is down for maintenance
#     or experiencing issues.
#     """

#     def __init__(
#         self, 
#         message: str = "Service temporarily unavailable", 
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
