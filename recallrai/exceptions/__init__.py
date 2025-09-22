"""
Exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError
from .auth import AuthenticationError
from .network import TimeoutError, ConnectionError
from .server import InternalServerError, RateLimitError
from .sessions import SessionNotFoundError, InvalidSessionStateError
from .users import UserNotFoundError, UserAlreadyExistsError, InvalidCategoriesError
from .validation import ValidationError
from .merge_conflicts import (
    MergeConflictError, 
    MergeConflictNotFoundError, 
    MergeConflictAlreadyResolvedError,
    MergeConflictInvalidQuestionsError,
    MergeConflictMissingAnswersError,
    MergeConflictInvalidAnswerError,
)

__all__ = [
    "RecallrAIError",
    "AuthenticationError",
    "TimeoutError", 
    "ConnectionError",
    "InternalServerError",
    "RateLimitError",
    "SessionNotFoundError", 
    "InvalidSessionStateError",
    "UserNotFoundError", 
    "UserAlreadyExistsError",
    "InvalidCategoriesError",
    "ValidationError",
    "MergeConflictError",
    "MergeConflictNotFoundError",
    "MergeConflictAlreadyResolvedError",
    "MergeConflictInvalidQuestionsError",
    "MergeConflictMissingAnswersError",
    "MergeConflictInvalidAnswerError",
]
