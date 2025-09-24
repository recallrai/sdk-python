"""
Authentication-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError


class AuthenticationError(RecallrAIError):
    """
    Raised when there is an authentication issue with the API key.
    
    This exception is typically raised when the API key is invalid,
    has been revoked, or doesn't have the necessary permissions.
    """

    def __init__(
        self, 
        message: str = "Invalid API key or authentication failed.", 
        http_status: int = 401,
    ):
        super().__init__(message, http_status)
