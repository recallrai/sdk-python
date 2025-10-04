"""
User-related data models for the RecallrAI SDK.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from pydantic import BaseModel, Field
from ..utils import HTTPClient
if TYPE_CHECKING:
    from ..user import User


class UserModel(BaseModel):
    """Represents a user in the RecallrAI system."""
    
    user_id: str = Field(..., description="Unique identifier for the user.")
    metadata: Dict[str, Any] = Field(..., description="Custom metadata for the user.")
    created_at: datetime = Field(..., description="When the user was created.")
    last_active_at: datetime = Field(..., description="When the user was last active.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "UserModel":
        """
        Create a UserModel instance from an API response.

        Args:
            data: API response data.

        Returns:
            A UserModel instance.
        """
        if "user" in data:
            user_data = data["user"]
        else:
            user_data = data

        return cls(
            user_id=user_data["user_id"],
            metadata=user_data.get("metadata", {}),
            created_at=user_data["created_at"],
            last_active_at=user_data["last_active_at"],
        )


class UserList(BaseModel):
    """Represents a paginated list of users."""

    users: List["User"] = Field(..., description="List of users.")
    total: int = Field(..., description="Total number of users.")
    has_more: bool = Field(..., description="Whether there are more users to fetch.")

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], http_client: HTTPClient) -> "UserList":
        """
        Create a UserList instance from an API response.

        Args:
            data: API response data.

        Returns:
            A UserList instance.
        """
        from ..user import User
        return cls(
            users=[
                User(http_client, UserModel.from_api_response(user)) for user in data["users"]
            ],
            total=data["total"],
            has_more=data["has_more"],
        )


class MemoryVersionInfo(BaseModel):
    """Information about a specific version of a memory."""
    
    version_number: int = Field(..., description="Version number (1 = oldest, N = current)")
    content: str = Field(..., description="Content of this version")
    created_at: datetime = Field(..., description="When this version was created")
    expired_at: datetime = Field(..., description="When this version expired")
    expiration_reason: str = Field(..., description="Why this version expired (NewMemoryVersionCreationReason enum)")

    class Config:
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class MemoryRelationship(BaseModel):
    """Connected memory information."""
    
    memory_id: str = Field(..., description="ID of the connected memory")
    content: str = Field(..., description="Brief content for context")

    class Config:
        frozen = True


class UserMemoryItem(BaseModel):
    """Complete memory information with all metadata."""

    memory_id: str = Field(..., description="ID of the current/latest version")
    categories: List[str] = Field(..., description="Memory categories")
    content: str = Field(..., description="Current version content")
    created_at: datetime = Field(..., description="When the latest version was created")
    
    # Version information
    version_number: int = Field(..., description="Which version this is (e.g., 3 means 3rd version)")
    total_versions: int = Field(..., description="How many versions exist total")
    has_previous_versions: bool = Field(..., description="If total_versions > 1")
    
    # Version history (only if requested)
    previous_versions: Optional[List[MemoryVersionInfo]] = Field(None, description="Memories connected via prev_version_id")
    
    # Relationships (only if requested)
    connected_memories: Optional[List[MemoryRelationship]] = Field(None, description="Memories connected via ProjectUserMemoryConnections")
    
    # Merge conflict info
    merge_conflict_in_progress: bool = Field(..., description="Whether a merge conflict is in progress")
    
    # Session info
    session_id: str = Field(..., description="Which session created this version")

    class Config:
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class UserMemoriesList(BaseModel):
    """Represents a paginated list of user memories."""

    items: List[UserMemoryItem]
    total: int
    has_more: bool

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "UserMemoriesList":
        return cls(
            items=[UserMemoryItem(**item) for item in data["items"]],
            total=data["total"],
            has_more=data["has_more"],
        )


class UserMessage(BaseModel):
    """Represents a single message from a user's conversation history."""

    role: str = Field(..., description="Role of the message sender (user or assistant).")
    content: str = Field(..., description="Content of the message.")
    timestamp: datetime = Field(..., description="When the message was sent.")
    session_id: str = Field(..., description="ID of the session this message belongs to.")

    class Config:
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class UserMessagesList(BaseModel):
    """Represents a list of user messages."""

    messages: List[UserMessage] = Field(..., description="List of user messages.")

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "UserMessagesList":
        """
        Create a UserMessagesList instance from an API response.

        Args:
            data: API response data.

        Returns:
            A UserMessagesList instance.
        """
        return cls(
            messages=[UserMessage(**message) for message in data["messages"]]
        )
