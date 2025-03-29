"""
Users-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .base import RecallrAIError

class UserError(RecallrAIError):
    """
    Base class for user-related exceptions.
    
    This exception is raised for errors related to user management
    in the RecallrAI API.
    """

    def __init__(
        self, 
        message: str = "User error occurred", 
        code: str = "user_error",
        http_status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)

class UserNotFoundError(UserError):
    """
    Raised when a user is not found.
    
    This exception is typically raised when trying to access or modify
    a user that doesn't exist.
    """
    def __init__(
        self, 
        user_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "user_not_found",
        http_status: int = 404,
        details: Optional[Dict[str, Any]] = None
    ):
        message = message or f"User{f' {user_id}' if user_id else ''} not found"
        super().__init__(message, code, http_status, details)
        self.user_id = user_id

class UserAlreadyExistsError(UserError):
    """
    Raised when a user already exists.
    
    This exception is typically raised when trying to create a user
    that already exists in the system.
    """
    def __init__(
        self, 
        user_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "user_already_exists",
        http_status: int = 409,
        details: Optional[Dict[str, Any]] = None
    ):
        message = message or f"User{f' {user_id}' if user_id else ''} already exists"
        super().__init__(message, code, http_status, details)
        self.user_id = user_id
