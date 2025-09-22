"""
Merge conflicts-related exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError

class MergeConflictError(RecallrAIError):
    """
    Base class for merge conflict-related exceptions.
    
    This exception is raised for errors related to merge conflict management
    in the RecallrAI API.
    """

    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class MergeConflictNotFoundError(MergeConflictError):
    """
    Raised when a merge conflict is not found.
    
    This exception is typically raised when trying to access or modify
    a merge conflict that doesn't exist.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)

class MergeConflictAlreadyResolvedError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict that is already resolved.
    
    This exception is typically raised when trying to resolve a merge conflict
    that has already been processed.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)


class MergeConflictInvalidQuestionsError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with invalid questions.
    
    This exception is raised when the provided questions don't match the 
    original clarifying questions for the merge conflict.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)


class MergeConflictMissingAnswersError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with missing answers.
    
    This exception is raised when not all required clarifying questions 
    have been answered.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)


class MergeConflictInvalidAnswerError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with invalid answer options.
    
    This exception is raised when the provided answer is not one of the 
    valid options for a question.
    """
    def __init__(self, message: str, http_status: int):
        super().__init__(message, http_status)
