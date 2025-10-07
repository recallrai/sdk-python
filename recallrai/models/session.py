"""
Session-related data models for the RecallrAI SDK.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List
from pydantic import BaseModel, Field
from ..utils import HTTPClient
if TYPE_CHECKING:
    from ..session import Session

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
    role: MessageRole = Field(..., description="Role of the message sender (user or assistant).")
    content: str = Field(..., description="Content of the message.")
    timestamp: datetime = Field(..., description="When the message was sent.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class SessionMessagesList(BaseModel):
    """
    Represents a paginated list of messages in a session.
    """

    messages: List[Message] = Field(..., description="List of messages in the page.")
    total: int = Field(..., description="Total number of messages in the session.")
    has_more: bool = Field(..., description="Whether there are more messages to fetch.")

    class Config:
        frozen = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "SessionMessagesList":
        return cls(
            messages=[Message(**msg) for msg in data["messages"]],
            total=data["total"],
            has_more=data["has_more"],
        )


class SessionStatus(str, enum.Enum):
    """
    Status of a session.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    INSUFFICIENT_BALANCE = "insufficient_balance"


class SessionModel(BaseModel):
    """
    Represents a conversation session.
    """
    session_id: str = Field(..., description="Unique identifier for the session.")
    status: SessionStatus = Field(..., description="Current status of the session.")
    created_at: datetime = Field(..., description="When the session was created.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional metadata for the session.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "SessionModel":
        """
        Create a SessionModel instance from an API response.

        Args:
            data: API response data.

        Returns:
            A SessionModel instance.
        """
        if "session" in data:
            session_data = data["session"]
        else:
            session_data = data
        return cls(
            session_id=session_data["session_id"],
            status=session_data["status"],
            created_at=session_data["created_at"],
            metadata=session_data["metadata"],
        )


class SessionList(BaseModel):
    """
    Represents a paginated list of sessions.
    """
    sessions: List["Session"] = Field(..., description="List of sessions.")
    total: int = Field(..., description="Total number of sessions.")
    has_more: bool = Field(..., description="Whether there are more sessions to fetch.")

    class Config:
        """Pydantic configuration."""
        frozen = True
        arbitrary_types_allowed = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], user_id: str, http_client: HTTPClient) -> "SessionList":
        """
        Create a SessionList instance from an API response.

        Args:
            data: API response data.

        Returns:
            A SessionList instance.
        """
        from ..session import Session
        return cls(
            sessions=[
                Session(http_client, user_id, SessionModel.from_api_response(session)) for session in data["sessions"]
            ],
            total=data["total"],
            has_more=data["has_more"],
        )

class RecallStrategy(str, enum.Enum):
    """
    Type of recall strategy.
    """
    LOW_LATENCY = "low_latency"
    BALANCED = "balanced"
    DEEP = "deep"

class Context(BaseModel):
    """
    Represents the context for a session.
    """
    context: str = Field(..., description="The context for the session.")

    class Config:
        """Pydantic configuration."""
        frozen = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "Context":
        """
        Create a Context instance from an API response.

        Args:
            data: API response data.

        Returns:
            A Context instance.
        """
        return cls(
            context=data["context"],
        )
