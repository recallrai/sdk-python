"""
User-related data models for the RecallrAI SDK.
"""

from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field


class User(BaseModel):
    """Represents a user in the RecallrAI system."""
    
    user_id: str = Field(..., description="Unique identifier for the user")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata for the user")
    created_at: datetime = Field(..., description="When the user was created")
    last_active_at: datetime = Field(..., description="When the user was last active")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "User":
        """
        Create a User instance from an API response.

        Args:
            data: API response data

        Returns:
            A User instance
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
    
    users: list[User] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    has_more: bool = Field(..., description="Whether there are more users to fetch")

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "UserList":
        """
        Create a UserList instance from an API response.

        Args:
            data: API response data

        Returns:
            A UserList instance
        """
        return cls(
            users=[User.from_api_response({"user": user}) for user in data["users"]],
            total=data["total"],
            has_more=data["has_more"],
        )
