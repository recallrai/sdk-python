"""
Validation-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError


class ValidationError(RecallrAIError):
    """
    Raised when request parameters fail validation.
    
    This exception is raised when the API rejects a request
    due to invalid or missing parameters.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)
