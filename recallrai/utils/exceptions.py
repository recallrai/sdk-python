# Path: recallrai/exceptions.py
# Description: Custom exceptions for the RecallrAI SDK

"""
Custom exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional


class RecallrAIError(Exception):
    """Base exception for all RecallrAI SDK errors."""

    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        """
        Initialize a RecallrAI error.

        Args:
            message: A human-readable error message
            code: An optional error code
            details: Optional additional details about the error
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(RecallrAIError):
    """Raised when there is an authentication issue with the API key or project ID."""
    pass


class NotFoundError(RecallrAIError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(RecallrAIError):
    """Raised when the API rejects a request due to validation errors."""
    pass


class RateLimitError(RecallrAIError):
    """Raised when the API rate limit has been exceeded."""
    pass


class ServerError(RecallrAIError):
    """Raised when the API encounters an unexpected server error."""
    pass


class BadRequestError(RecallrAIError):
    """Raised when the API rejects a request due to invalid parameters."""
    pass


class SessionProcessingError(RecallrAIError):
    """Raised when there is an error processing a session."""
    pass
