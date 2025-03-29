"""
Base exception classes for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional


class RecallrAIError(Exception):
    """Base exception for all RecallrAI SDK errors."""

    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None, 
        http_status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a RecallrAI error.

        Args:
            message: A human-readable error message
            code: An optional error code
            http_status: The HTTP status code that triggered this error
            details: Optional additional details about the error
        """
        self.message = message
        self.code = code
        self.http_status = http_status
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return a string representation of the error."""
        if self.code:
            return f"{self.code}: {self.message}"
        return self.message
