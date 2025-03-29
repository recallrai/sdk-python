"""
Exceptions for the RecallrAI SDK.
"""

from .auth import AuthenticationError
from .base import RecallrAIError
from .network import NetworkError, TimeoutError, ConnectionError
from .server import ServerError, InternalServerError
from .sessions import SessionError, SessionNotFoundError, InvalidSessionStateError
from .users import UserError, UserNotFoundError, UserAlreadyExistsError
from .validation import ValidationError

__all__ = [
    "RecallrAIError",
    "AuthenticationError",
    "NetworkError", 
    "TimeoutError", 
    "ConnectionError",
    "ServerError", 
    "InternalServerError",
    "SessionError", 
    "SessionNotFoundError", 
    "InvalidSessionStateError",
    "UserError", 
    "UserNotFoundError", 
    "UserAlreadyExistsError",
    "ValidationError",
]
