"""
Session-related data models for the RecallrAI SDK.
"""

import enum
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from ..utils import HTTPClient
if TYPE_CHECKING:
    from ..session import Session
    from ..async_session import AsyncSession

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
    FAILED = "failed"
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
    sessions: List[Union["Session", "AsyncSession"]] = Field(..., description="List of sessions.")
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
            user_id: User ID who owns these sessions.
            http_client: HTTP client for making API requests.

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

    @classmethod
    def from_api_response_async(cls, data: Dict[str, Any], user_id: str, http_client: Any) -> "SessionList":
        """
        Create a SessionList instance from an API response for async client.

        Args:
            data: API response data.
            user_id: User ID who owns these sessions.
            http_client: Async HTTP client for making API requests.

        Returns:
            A SessionList instance with async sessions.
        """
        from ..async_session import AsyncSession
        return cls(
            sessions=[
                AsyncSession(http_client, user_id, SessionModel.from_api_response(session)) for session in data["sessions"]
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
    AGENTIC = "agentic"
    AUTO = "auto"

class DateRangeFilterType(str, enum.Enum):
    """
    Type of date field to filter on when querying memories.
    """
    EVENT_DATE = "event_date"
    CREATED_AT = "created_at"

class QueryDateRangeFilter(BaseModel):
    """
    Date range filter extracted from a user query.
    """
    filter_type: DateRangeFilterType = Field(..., description="Type of date filter (event_date or created_at).")
    start_date: datetime = Field(..., description="Start of the date range (ISO 8601 timestamp).")
    end_date: datetime = Field(..., description="End of the date range (ISO 8601 timestamp).")

class ContextMetadata(BaseModel):
    """
    Metadata for context generation, including IDs of memories and sessions that contributed.
    """
    memory_ids: Optional[List[str]] = Field(None, description="IDs of memories that contributed to the context.")
    session_ids: Optional[List[str]] = Field(None, description="IDs of sessions that contributed to the context.")
    agent_reasoning: Optional[str] = Field(None, description="Agent's reasoning process. Only populated for agentic recall strategy.")
    vector_search_queries: Optional[List[str]] = Field(None, description="Vector search queries generated for recall.")
    keywords: Optional[List[str]] = Field(None, description="Keywords extracted for recall.")
    session_summaries_search_queries: Optional[List[str]] = Field(None, description="Queries used to search session summaries.")
    date_range_filters: Optional[List[QueryDateRangeFilter]] = Field(None, description="Date range filters extracted from the query.")

    class Config:
        """Pydantic configuration."""
        frozen = True

class ContextResponse(BaseModel):
    """
    Represents a context response from the API.
    This model is used for both streaming and non-streaming responses.
    """
    is_final: bool = Field(..., description="Whether this is the final response.")
    status_update_message: Optional[str] = Field(None, description="Human-readable status update for streaming.")
    error_message: Optional[str] = Field(None, description="Error message, if any.")
    context: Optional[str] = Field(None, description="Final context when is_final is True.")
    metadata: Optional[ContextMetadata] = Field(None, description="Metadata including memory and session IDs.")

    class Config:
        """Pydantic configuration."""
        frozen = True

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> "ContextResponse":
        """
        Create a ContextResponse instance from an API response.

        Args:
            data: API response data.

        Returns:
            A ContextResponse instance.
        """
        metadata_data = data.get("metadata")
        metadata = None
        if metadata_data:
            metadata = ContextMetadata(
                memory_ids=metadata_data.get("memory_ids"),
                session_ids=metadata_data.get("session_ids"),
                agent_reasoning=metadata_data.get("agent_reasoning"),
                vector_search_queries=metadata_data.get("vector_search_queries"),
                keywords=metadata_data.get("keywords"),
                session_summaries_search_queries=metadata_data.get("session_summaries_search_queries"),
                date_range_filters=[
                    QueryDateRangeFilter(**item)
                    for item in metadata_data.get("date_range_filters", [])
                ] if metadata_data.get("date_range_filters") else None,
            )
        
        return cls(
            is_final=data.get("is_final", False),
            status_update_message=data.get("status_update_message"),
            error_message=data.get("error_message"),
            context=data.get("context"),
            metadata=metadata,
        )
