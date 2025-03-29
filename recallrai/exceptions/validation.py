"""
Validation-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional, Union
from .base import RecallrAIError


class ValidationError(RecallrAIError):
    """
    Raised when request parameters fail validation.
    
    This exception is raised when the API rejects a request
    due to invalid or missing parameters.
    """

    def __init__(
        self, 
        message: str = "Validation error", 
        code: str = "validation_error",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)
