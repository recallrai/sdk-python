"""
User-related data models for the RecallrAI SDK.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List
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


class UserMemoryItem(BaseModel):
    """Represents a single memory item for a user."""

    memory_id: str
    categories: List[str]
    content: str
    created_at: datetime

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
