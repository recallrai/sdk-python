"""
Users-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError

class UserError(RecallrAIError):
    """
    Base class for user-related exceptions.
    
    This exception is raised for errors related to user management
    in the RecallrAI API.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class UserNotFoundError(UserError):
    """
    Raised when a user is not found.
    
    This exception is typically raised when trying to access or modify
    a user that doesn't exist.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class UserAlreadyExistsError(UserError):
    """
    Raised when a user already exists.
    
    This exception is typically raised when trying to create a user
    that already exists in the system.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class InvalidCategoriesError(UserError):
    """
    Raised when invalid categories are provided for user memories.
    
    This exception is typically raised when trying to filter memories
    by categories that don't exist in the project.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)
