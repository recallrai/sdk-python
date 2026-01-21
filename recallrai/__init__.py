"""
RecallrAI Python SDK.

This package provides a Python interface to interact with the RecallrAI API.
"""

from .client import RecallrAI
from .user import User
from .session import Session
from .merge_conflict import MergeConflict
from .async_client import AsyncRecallrAI
from .async_user import AsyncUser
from .async_session import AsyncSession
from .async_merge_conflict import AsyncMergeConflict

__version__ = "0.5.5"

__all__ = [
    "RecallrAI",
    "User",
    "Session",
    "MergeConflict",
    "AsyncRecallrAI",
    "AsyncUser",
    "AsyncSession",
    "AsyncMergeConflict",
]

# Fix pydantic v2 import issues by rebuilding models
from .user import User as _User
from .async_user import AsyncUser as _AsyncUser
from .models.user import UserList as _UserListModel
_UserListModel.model_rebuild()
del _User, _AsyncUser, _UserListModel

from .session import Session as _Session
from .async_session import AsyncSession as _AsyncSession
from .models.session import SessionList as _SessionListModel
_SessionListModel.model_rebuild()
del _Session, _AsyncSession, _SessionListModel

from .merge_conflict import MergeConflict as _MergeConflict
from .async_merge_conflict import AsyncMergeConflict as _AsyncMergeConflict
from .models.merge_conflict import MergeConflictList as _MergeConflictListModel
_MergeConflictListModel.model_rebuild()
del _MergeConflict, _AsyncMergeConflict, _MergeConflictListModel
