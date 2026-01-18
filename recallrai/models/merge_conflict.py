"""
Merge conflict-related data models for the RecallrAI SDK.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from ..utils import HTTPClient

if TYPE_CHECKING:
    from ..merge_conflict import MergeConflict
    from ..async_merge_conflict import AsyncMergeConflict


class MergeConflictStatus(str, enum.Enum):
    """
    Status of a merge conflict.
    """
    PENDING = "PENDING"
    IN_QUEUE = "IN_QUEUE"
    RESOLVING = "RESOLVING"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"


class MergeConflictConflictingMemory(BaseModel):
    """
    Represents a memory involved in a merge conflict.
    """
    memory_id: str = Field(..., description="Unique identifier for the memory.")
    content: str = Field(..., description="Content of the conflicting memory.")
    reason: str = Field(..., description="Reason why this memory conflicts.")
    event_date_start: datetime = Field(..., description="When the event described in the memory started.")
    event_date_end: datetime = Field(..., description="When the event described in the memory ended.")
    created_at: datetime = Field(..., description="When this memory was created.")

    class Config:
        """Pydantic configuration."""
        frozen = True


class MergeConflictQuestion(BaseModel):
    """
    Represents a clarifying question for merge conflict resolution.
    """
    question: str = Field(..., description="The clarifying question.")
    options: List[str] = Field(..., description="Available answer options.")

    class Config:
        """Pydantic configuration."""
        frozen = True


class MergeConflictAnswer(BaseModel):
    """
    Represents an answer to a clarifying question.
    """
    question: str = Field(..., description="The question being answered.")
    answer: str = Field(..., description="The selected answer.")
    message: Optional[str] = Field(None, description="Optional additional message.")

    class Config:
        """Pydantic configuration."""
        frozen = True


class MergeConflictNewMemory(BaseModel):
    """
    Represents a new memory created from resolving a merge conflict.
    """
    memory_id: str = Field(..., description="Unique identifier for the new memory.")
    content: str = Field(..., description="Content of the new memory.")
    event_date_start: datetime = Field(..., description="When the event described in the memory started.")
    event_date_end: datetime = Field(..., description="When the event described in the memory ended.")
    created_at: datetime = Field(..., description="When this memory was created.")

    class Config:
        """Pydantic configuration."""
        frozen = True


class MergeConflictModel(BaseModel):
    """
    Represents a merge conflict in the RecallrAI system.
    """
    id: str = Field(..., description="Unique identifier for the merge conflict.")
    project_user_session_id: str = Field(..., description="Session ID where the conflict occurred.")
    new_memory_content: Optional[str] = Field(None, description="New memory content that caused the conflict (for unresolved conflicts).")
    new_memories: Optional[List[MergeConflictNewMemory]] = Field(None, description="New memories created from resolution (for resolved conflicts).")
    conflicting_memories: List[MergeConflictConflictingMemory] = Field(..., description="Existing memories that conflict.")
    clarifying_questions: List[MergeConflictQuestion] = Field(..., description="Questions to resolve the conflict.")
    status: MergeConflictStatus = Field(..., description="Current status of the conflict.")
    resolution_data: Optional[Dict[str, Any]] = Field(None, description="Resolution data if resolved.")
    created_at: datetime = Field(..., description="When the conflict was created.")
    resolved_at: Optional[datetime] = Field(None, description="When the conflict was resolved.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "MergeConflictModel":
        """
        Create a MergeConflictModel instance from an API response.

        Args:
            data: API response data.

        Returns:
            A MergeConflictModel instance.
        """
        conflict_data = data.get("conflict", data)
        
        return cls(
            id=conflict_data["id"],
            project_user_session_id=conflict_data["project_user_session_id"],
            new_memory_content=conflict_data.get("new_memory_content"),
            new_memories=[
                MergeConflictNewMemory(**memory) for memory in conflict_data["new_memories"]
            ] if conflict_data.get("new_memories") else None,
            conflicting_memories=[
                MergeConflictConflictingMemory(**memory) for memory in conflict_data["conflicting_memories"]
            ],
            clarifying_questions=[
                MergeConflictQuestion(**question) for question in conflict_data["clarifying_questions"]
            ],
            status=MergeConflictStatus(conflict_data["status"]),
            resolution_data=conflict_data.get("resolution_data"),
            created_at=conflict_data["created_at"],
            resolved_at=conflict_data.get("resolved_at"),
        )


class MergeConflictList(BaseModel):
    """
    Represents a paginated list of merge conflicts.
    """
    conflicts: List[Union["MergeConflict", "AsyncMergeConflict"]] = Field(..., description="List of merge conflicts.")
    total: int = Field(..., description="Total number of conflicts.")
    has_more: bool = Field(..., description="Whether there are more conflicts to fetch.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        arbitrary_types_allowed = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], user_id: str, http_client: HTTPClient) -> "MergeConflictList":
        """
        Create a MergeConflictList instance from an API response.

        Args:
            data: API response data.
            user_id: User ID who owns these conflicts.
            http_client: HTTP client for making API requests.

        Returns:
            A MergeConflictList instance.
        """
        from ..merge_conflict import MergeConflict
        
        return cls(
            conflicts=[
                MergeConflict(http_client, user_id, MergeConflictModel.from_api_response(conflict))
                for conflict in data["conflicts"]
            ],
            total=data["total"],
            has_more=data["has_more"],
        )

    @classmethod
    def from_api_response_async(cls, data: Dict[str, Any], user_id: str, http_client: Any) -> "MergeConflictList":
        """
        Create a MergeConflictList instance from an API response for async client.

        Args:
            data: API response data.
            user_id: User ID who owns these conflicts.
            http_client: Async HTTP client for making API requests.

        Returns:
            A MergeConflictList instance with async conflicts.
        """
        from ..async_merge_conflict import AsyncMergeConflict
        
        return cls(
            conflicts=[
                AsyncMergeConflict(http_client, user_id, MergeConflictModel.from_api_response(conflict))
                for conflict in data["conflicts"]
            ],
            total=data["total"],
            has_more=data["has_more"],
        )
