"""
Network-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError


class NetworkError(RecallrAIError):
    """
    Base class for network-related exceptions.
    
    This exception is raised for errors related to network connectivity
    and communication with the RecallrAI API.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)


class TimeoutError(NetworkError):
    """
    Raised when a request times out.
    
    This exception is raised when a request to the RecallrAI API
    takes longer than the configured timeout.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)


class ConnectionError(NetworkError):
    """
    Raised when a connection error occurs.
    
    This exception is raised when there's an issue connecting to
    the RecallrAI API, such as DNS resolution issues or network unavailability.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)
