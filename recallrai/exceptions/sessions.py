"""
Sessions-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .base import RecallrAIError

class SessionError(RecallrAIError):
    """
    Base class for session-related exceptions.
    
    This exception is raised for errors related to session management
    in the RecallrAI API.
    """

    def __init__(
        self, 
        message: str = "Session error occurred", 
        code: str = "session_error",
        http_status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)

class InvalidSessionStateError(SessionError):
    """
    Raised when a session is in an invalid state.
    
    This exception is typically raised when trying to perform an action
    on a session that is not in the expected state.
    """

    def __init__(
        self, 
        message: str = "Invalid session state", 
        code: str = "invalid_session_state",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)

class SessionNotFoundError(SessionError):
    """
    Raised when a session is not found.
    
    This exception is typically raised when trying to access or modify
    a session that doesn't exist.
    """

    def __init__(
        self, 
        session_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "session_not_found",
        http_status: int = 404,
        details: Optional[Dict[str, Any]] = None
    ):
        message = message or f"Session{f' {session_id}' if session_id else ''} not found"
        super().__init__(message, code, http_status, details)
        self.session_id = session_id
