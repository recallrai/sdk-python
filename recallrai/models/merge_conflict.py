"""
Merge conflict-related data models for the RecallrAI SDK.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..utils import HTTPClient

if TYPE_CHECKING:
    from ..merge_conflict import MergeConflict


class MergeConflictStatus(str, enum.Enum):
    """
    Status of a merge conflict.
    """
    PENDING = "PENDING"
    IN_QUEUE = "IN_QUEUE"
    RESOLVING = "RESOLVING"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"


class MergeConflictMemory(BaseModel):
    """
    Represents a memory involved in a merge conflict.
    """
    content: str = Field(..., description="Content of the conflicting memory.")
    reason: str = Field(..., description="Reason why this memory conflicts.")

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


class MergeConflictModel(BaseModel):
    """
    Represents a merge conflict in the RecallrAI system.
    """
    id: str = Field(..., description="Unique identifier for the merge conflict.")
    custom_user_id: str = Field(..., description="User ID who owns this conflict.")
    project_user_session_id: str = Field(..., description="Session ID where the conflict occurred.")
    new_memory_content: str = Field(..., description="New memory content that caused the conflict.")
    conflicting_memories: List[MergeConflictMemory] = Field(..., description="Existing memories that conflict.")
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
            custom_user_id=conflict_data["custom_user_id"],
            project_user_session_id=conflict_data["project_user_session_id"],
            new_memory_content=conflict_data["new_memory_content"],
            conflicting_memories=[
                MergeConflictMemory(**memory) for memory in conflict_data["conflicting_memories"]
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
    conflicts: List["MergeConflict"] = Field(..., description="List of merge conflicts.")
    total: int = Field(..., description="Total number of conflicts.")
    has_more: bool = Field(..., description="Whether there are more conflicts to fetch.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        arbitrary_types_allowed = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], http_client: HTTPClient, user_id: str) -> "MergeConflictList":
        """
        Create a MergeConflictList instance from an API response.

        Args:
            data: API response data.
            http_client: HTTP client for making API requests.
            user_id: User ID who owns these conflicts.

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
