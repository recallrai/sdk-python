# Path: recallrai/__init__.py
# Description: Package initialization file with SDK version and main class exports

"""
RecallrAI Python SDK

This package provides a Python interface to interact with the RecallrAI API.
"""

from .client import RecallrAI
from .user import User
from .session import Session

__all__ = [
    "RecallrAI",
    "User",
    "Session",
]
