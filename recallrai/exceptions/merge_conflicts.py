"""
Merge conflicts-related exceptions for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .base import RecallrAIError

class MergeConflictError(RecallrAIError):
    """
    Base class for merge conflict-related exceptions.
    
    This exception is raised for errors related to merge conflict management
    in the RecallrAI API.
    """

    def __init__(
        self, 
        message: str = "Merge conflict error occurred", 
        code: str = "merge_conflict_error",
        http_status: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, code, http_status, details)

class MergeConflictNotFoundError(MergeConflictError):
    """
    Raised when a merge conflict is not found.
    
    This exception is typically raised when trying to access or modify
    a merge conflict that doesn't exist.
    """
    def __init__(
        self, 
        conflict_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "merge_conflict_not_found",
        http_status: int = 404,
        details: Optional[Dict[str, Any]] = None
    ):
        message = message or f"Merge conflict{f' {conflict_id}' if conflict_id else ''} not found"
        super().__init__(message, code, http_status, details)
        self.conflict_id = conflict_id

class MergeConflictAlreadyResolvedError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict that is already resolved.
    
    This exception is typically raised when trying to resolve a merge conflict
    that has already been processed.
    """
    def __init__(
        self, 
        conflict_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "merge_conflict_already_resolved",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        message = message or f"Merge conflict{f' {conflict_id}' if conflict_id else ''} is already resolved"
        super().__init__(message, code, http_status, details)
        self.conflict_id = conflict_id