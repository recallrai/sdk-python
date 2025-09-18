"""
Exceptions for the RecallrAI SDK.
"""

from .base import RecallrAIError
from .auth import AuthenticationError
from .network import TimeoutError, ConnectionError
from .server import InternalServerError, RateLimitError
from .sessions import SessionNotFoundError, InvalidSessionStateError
from .users import UserNotFoundError, UserAlreadyExistsError
from .validation import ValidationError

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
    "ValidationError",
]
