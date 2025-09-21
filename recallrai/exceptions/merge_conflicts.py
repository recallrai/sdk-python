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


class MergeConflictInvalidQuestionsError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with invalid questions.
    
    This exception is raised when the provided questions don't match the 
    original clarifying questions for the merge conflict.
    """
    def __init__(
        self, 
        invalid_questions: Optional[list] = None,
        conflict_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "merge_conflict_invalid_questions",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        if not message:
            if invalid_questions:
                message = f"Invalid questions provided: {invalid_questions}"
            else:
                message = "The provided questions do not match the original questions"
        super().__init__(message, code, http_status, details)
        self.invalid_questions = invalid_questions
        self.conflict_id = conflict_id


class MergeConflictMissingAnswersError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with missing answers.
    
    This exception is raised when not all required clarifying questions 
    have been answered.
    """
    def __init__(
        self, 
        missing_questions: Optional[list] = None,
        conflict_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "merge_conflict_missing_answers",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        if not message:
            if missing_questions:
                message = f"Missing answers for questions: {missing_questions}"
            else:
                message = "Not all required questions have been answered"
        super().__init__(message, code, http_status, details)
        self.missing_questions = missing_questions
        self.conflict_id = conflict_id


class MergeConflictInvalidAnswerError(MergeConflictError):
    """
    Raised when trying to resolve a merge conflict with invalid answer options.
    
    This exception is raised when the provided answer is not one of the 
    valid options for a question.
    """
    def __init__(
        self, 
        question: Optional[str] = None,
        invalid_answer: Optional[str] = None,
        valid_options: Optional[list] = None,
        conflict_id: Optional[str] = None,
        message: Optional[str] = None,
        code: str = "merge_conflict_invalid_answer",
        http_status: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        if not message:
            if question and invalid_answer and valid_options:
                message = f"Invalid answer '{invalid_answer}' for question '{question}'. Valid options are: {valid_options}"
            else:
                message = "The provided answer is not a valid option for the question"
        super().__init__(message, code, http_status, details)
        self.question = question
        self.invalid_answer = invalid_answer
        self.valid_options = valid_options
        self.conflict_id = conflict_id