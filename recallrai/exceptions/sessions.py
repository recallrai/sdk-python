"""
Sessions-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError

class SessionError(RecallrAIError):
    """
    Base class for session-related exceptions.
    
    This exception is raised for errors related to session management
    in the RecallrAI API.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class InvalidSessionStateError(SessionError):
    """
    Raised when a session is in an invalid state.
    
    This exception is typically raised when trying to perform an action
    on a session that is not in the expected state.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class SessionNotFoundError(SessionError):
    """
    Raised when a session is not found.
    
    This exception is typically raised when trying to access or modify
    a session that doesn't exist.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)
