"""
Session-related data models for the RecallrAI SDK.
"""

import enum, uuid
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class MessageRole(str, enum.Enum):
    """
    Message role in a conversation.
    """
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """
    Represents a message in a conversation session.
    """
    role: MessageRole = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(..., description="When the message was sent")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class SessionStatus(str, enum.Enum):
    """
    Status of a session.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"


class SessionModel(BaseModel):
    """
    Represents a conversation session.
    """
    session_id: uuid.UUID = Field(..., description="Unique identifier for the session")
    status: SessionStatus = Field(..., description="Current status of the session")
    created_at: datetime = Field(..., description="When the session was created")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            uuid.UUID: lambda id: str(id)
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "SessionModel":
        """
        Create a SessionModel instance from an API response.

        Args:
            data: API response data

        Returns:
            A SessionModel instance
        """
        return cls(
            session_id=data["session_id"],
            status=data.get("status", SessionStatus.PENDING),
            created_at=data.get("created_at", datetime.now()),
        )


class SessionList(BaseModel):
    """
    Represents a paginated list of sessions.
    """
    sessions: List[SessionModel] = Field(..., description="List of sessions")
    total: int = Field(..., description="Total number of sessions")
    has_more: bool = Field(..., description="Whether there are more sessions to fetch")

    class Config:
        """Pydantic configuration."""
        frozen = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "SessionList":
        """
        Create a SessionList instance from an API response.

        Args:
            data: API response data

        Returns:
            A SessionList instance
        """
        return cls(
            sessions=[SessionModel.from_api_response(session) for session in data["sessions"]],
            total=data["total"],
            has_more=data["has_more"],
        )


class Context(BaseModel):
    """
    Represents the context for a session.
    """
    memory_used: bool = Field(..., description="Whether memory was used to generate the context")
    context: str = Field(..., description="The context for the session")

    class Config:
        """Pydantic configuration."""
        frozen = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Context":
        """
        Create a Context instance from an API response.

        Args:
            data: API response data

        Returns:
            A Context instance
        """
        return cls(
            memory_used=data["memory_used"],
            context=data["context"],
        )
