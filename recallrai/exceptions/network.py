"""
Network-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .base import RecallrAIError


class NetworkError(RecallrAIError):
    """
    Base class for network-related exceptions.
    
    This exception is raised for errors related to network connectivity
    and communication with the RecallrAI API.
    """

    def __init__(
        self, 
        message: str = "Network error occurred", 
        code: str = "network_error",
        http_status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)


class TimeoutError(NetworkError):
    """
    Raised when a request times out.
    
    This exception is raised when a request to the RecallrAI API
    takes longer than the configured timeout.
    """

    def __init__(
        self, 
        message: str = "Request timed out", 
        code: str = "timeout",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, None, details)


class ConnectionError(NetworkError):
    """
    Raised when a connection error occurs.
    
    This exception is raised when there's an issue connecting to
    the RecallrAI API, such as DNS resolution issues or network unavailability.
    """

    def __init__(
        self, 
        message: str = "Failed to connect to the RecallrAI API", 
        code: str = "connection_error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, None, details)
