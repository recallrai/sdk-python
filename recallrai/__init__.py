"""
RecallrAI Python SDK

This package provides a Python interface to interact with the RecallrAI API.
"""

from .client import RecallrAI
from .user import User
from .session import Session

with open("VERSION", "r") as version_file:
    __version__ = version_file.read().strip()

__all__ = [
    "RecallrAI",
    "User",
    "Session",
]
