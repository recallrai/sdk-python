# Path: recallrai/session.py
# Description: Session management class for the RecallrAI SDK

"""
Session management functionality for the RecallrAI SDK.
"""

from typing import List
from .utils import HTTPClient, RecallrAIError
from .models import (
    Context,
    Message,
    SessionStatus,
    MessageRole
)
from logging import getLogger

logger = getLogger(__name__)

class Session:
    """
    Manages a conversation session with RecallrAI.
    
    This class handles adding messages, retrieving context, and processing the session
    to update the user's memory.
    """

    def __init__(
        self,
        http_client: HTTPClient,
        user_id: str,
        session_id: str,
    ):
        """
        Initialize a session.

        Args:
            http_client: HTTP client for API communication
            user_id: ID of the user who owns this session
            session_id: Unique identifier for the session
        """
        self._http = http_client
        self.user_id = user_id
        self.session_id = session_id

    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the session.

        Args:
            message: Content of the user message

        Raises:
            BadRequestError: If the session is already processed
            NotFoundError: If the session or user is not found
        """
        # Check the status of session
        status = self.get_status()
        if status == SessionStatus.PROCESSED:
            raise RecallrAIError("Cannot add message to a session that has already been processed")
        elif status == SessionStatus.PROCESSING:
            raise RecallrAIError("Cannot add message to a session that is currently being processed")
        
        # Add the user message
        self._http.post(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/add-message",
            data={"message": message, "role": MessageRole.USER},
        )

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message to the session.

        Args:
            message: Content of the assistant message

        Raises:
            BadRequestError: If the session is already processed
            NotFoundError: If the session or user is not found
        """
        # Check the status of session
        status = self.get_status()
        if status == SessionStatus.PROCESSED:
            raise RecallrAIError("Cannot add message to a session that has already been processed")
        elif status == SessionStatus.PROCESSING:
            raise RecallrAIError("Cannot add message to a session that is currently being processed")
        
        # Add the assistant message
        self._http.post(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/add-message",
            data={"message": message, "role": MessageRole.ASSISTANT},
        )

    def get_context(self) -> Context:
        """
        Get the current context for this session.

        The context contains information from the user's memory that is relevant
        to the current conversation.

        Returns:
            Context information with the memory text and whether memory was used

        Raises:
            NotFoundError: If the session or user is not found
        """
        status = self.get_status()
        if status == SessionStatus.PROCESSED:
            logger.warning("Cannot add message to a session that has already been processed")
        elif status == SessionStatus.PROCESSING:
            logger.warning("Cannot add message to a session that is currently being processed")
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/context"
        )
        return Context.from_api_response(response)

    def process(self) -> None:
        """
        Process the session to update the user's memory.

        This method triggers the processing of the conversation to extract and update
        the user's memory.

        Raises:
            BadRequestError: If the session is already processed or being processed
            NotFoundError: If the session or user is not found
            SessionProcessingError: If there is an error during processing
        """
        # Check the status of session
        status = self.get_status()
        if status == SessionStatus.PROCESSED:
            raise RecallrAIError("Cannot process a session that has already been processed")
        elif status == SessionStatus.PROCESSING:
            raise RecallrAIError("Cannot process a session that is currently being processed")
        
        # Process the session
        self._http.post(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/process"
        )

    def get_status(self) -> SessionStatus:
        """
        Get the current status of the session.

        Returns:
            SessionStatus: The current status of the session

        Raises:
            NotFoundError: If the session or user is not found
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/status"
        )
        return SessionStatus(response["status"])

    def get_messages(self) -> List[Message]:
        """
        Get all messages in the session.

        Returns:
            List of messages in the session

        Raises:
            NotFoundError: If the session or user is not found
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/messages"
        )
        return [Message(**msg) for msg in response["messages"]]
