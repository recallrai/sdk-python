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

class InvalidCategoriesError(UserError):
    """
    Raised when invalid categories are provided for user memories.
    
    This exception is typically raised when trying to filter memories
    by categories that don't exist in the project.
    """
    def __init__(
        self, 
        invalid_categories: Optional[list] = None,
        message: Optional[str] = None,
        code: str = "invalid_categories",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        if invalid_categories and not message:
            categories_str = ", ".join(invalid_categories)
            message = f"The following categories do not exist: {categories_str}"
        else:
            message = message or "Invalid categories provided"
        super().__init__(message, code, http_status, details)
        self.invalid_categories = invalid_categories or []
