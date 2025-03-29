"""
Session management functionality for the RecallrAI SDK.
"""

from typing import List
from .utils import HTTPClient
from .models import (
    Context,
    Message,
    SessionStatus,
    MessageRole
)
from .exceptions import (
    UserNotFoundError,
    SessionNotFoundError,
    InvalidSessionStateError,
    RecallrAIError
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
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            InvalidSessionStateError: If the session is already processed or processing
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        self._add_message(message, MessageRole.USER)

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message to the session.

        Args:
            message: Content of the assistant message

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            InvalidSessionStateError: If the session is already processed or processing
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        self._add_message(message, MessageRole.ASSISTANT)

    def _add_message(self, message: str, role: MessageRole) -> None:
        """
        Internal helper to add a message to the session.
        
        Args:
            message: Content of the message
            role: Role of the message sender
            
        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            InvalidSessionStateError: If the session is already processed or processing
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.post(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/add-message",
            data={"message": message, "role": role.value},
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(user_id=self.user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code == 400:
            raise InvalidSessionStateError(
                message=f"Cannot add message to session with status {self.get_status()}",
            )
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to add message: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )

    def get_context(self) -> Context:
        """
        Get the current context for this session.

        The context contains information from the user's memory that is relevant
        to the current conversation.

        Returns:
            Context information with the memory text and whether memory was used

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/context"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(user_id=self.user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to get context: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
        status = self.get_status()
        if status == SessionStatus.PROCESSED:
            logger.warning("Cannot add message to a session that has already been processed")
        elif status == SessionStatus.PROCESSING:
            logger.warning("Cannot add message to a session that is currently being processed")
        return Context.from_api_response(response.json())

    def process(self) -> None:
        """
        Process the session to update the user's memory.

        This method triggers the processing of the conversation to extract and update
        the user's memory.

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            InvalidSessionStateError: If the session is already processed or being processed
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.post(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/process"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(user_id=self.user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code == 400:
            raise InvalidSessionStateError(
                message=f"{response.json().get('detail', f'Cannot process session with status {self.get_status()}')}",
            )
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to process session: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )

    def get_status(self) -> SessionStatus:
        """
        Get the current status of the session.

        Returns:
            SessionStatus: The current status of the session

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/status"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(user_id=self.user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to get session status: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
            
        return SessionStatus(response.json()["status"])

    def get_messages(self) -> List[Message]:
        """
        Get all messages in the session.

        Returns:
            List of messages in the session

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/messages"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(user_id=self.user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to get messages: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
            
        data = response.json()
        return [Message(**msg) for msg in data["messages"]]
