"""
Session management functionality for the RecallrAI SDK.
"""

from typing import Optional, Dict, Any
from .utils import HTTPClient
from .models import (
    # Context,
    SessionMessagesList,
    SessionModel,
    # SessionStatus,
    # MessageRole
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
        session_data: SessionModel,
    ):
        """
        Initialize a session.

        Args:
            http_client: HTTP client for API communication
            user_id: ID of the user who owns this session
            session_data: Initial session data from the API
        """
        self._http = http_client
        self._user_id = user_id
        self._session_data = session_data
        self.session_id = self._session_data.session_id
        self.status = self._session_data.status
        self.created_at = self._session_data.created_at
        self.metadata = self._session_data.metadata

    # def add_message(self, role: MessageRole, content: str) -> None:
    #     """
    #     Internal helper to add a message to the session.

    #     Args:
    #         role: Role of the message sender
    #         content: Content of the message

    #     Raises:
    #         UserNotFoundError: If the user is not found
    #         SessionNotFoundError: If the session is not found
    #         InvalidSessionStateError: If the session is already processed or processing
    #         AuthenticationError: If the API key or project ID is invalid
    #         InternalServerError: If the server encounters an error
    #         NetworkError: If there are network issues
    #         TimeoutError: If the request times out
    #         RecallrAIError: For other API-related errors
    #     """
    #     response = self._http.post(
    #         f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/add-message",
    #         data={"message": content, "role": role.value},
    #     )

    #     if response.status_code == 404:
    #         # Check if it's a user not found or session not found error
    #         detail = response.json().get('detail', '')
    #         if f"User {self.user_id} not found" in detail:
    #             raise UserNotFoundError(user_id=self.user_id)
    #         else:
    #             raise SessionNotFoundError(session_id=self.session_id)
    #     elif response.status_code == 400:
    #         raise InvalidSessionStateError(
    #             message=f"Cannot add message to session with status {self.get_status()}",
    #         )
    #     elif response.status_code != 200:
    #         raise RecallrAIError(
    #             message=f"Failed to add message: {response.json().get('detail', 'Unknown error')}",
    #             http_status=response.status_code
    #         )

    # def get_context(self) -> Context:
    #     """
    #     Get the current context for this session.

    #     The context contains information from the user's memory that is relevant
    #     to the current conversation.

    #     Returns:
    #         Context information with the memory text and whether memory was used

    #     Raises:
    #         UserNotFoundError: If the user is not found
    #         SessionNotFoundError: If the session is not found
    #         AuthenticationError: If the API key or project ID is invalid
    #         InternalServerError: If the server encounters an error
    #         NetworkError: If there are network issues
    #         TimeoutError: If the request times out
    #         RecallrAIError: For other API-related errors
    #     """
    #     response = self._http.get(
    #         f"/api/v1/users/{self.user_id}/sessions/{self.session_id}/context"
    #     )

    #     if response.status_code == 404:
    #         # Check if it's a user not found or session not found error
    #         detail = response.json().get('detail', '')
    #         if f"User {self.user_id} not found" in detail:
    #             raise UserNotFoundError(user_id=self.user_id)
    #         else:
    #             raise SessionNotFoundError(session_id=self.session_id)
    #     elif response.status_code != 200:
    #         raise RecallrAIError(
    #             message=f"Failed to get context: {response.json().get('detail', 'Unknown error')}",
    #             http_status=response.status_code
    #         )
    #     status = self.get_status()
    #     if status == SessionStatus.PROCESSED:
    #         logger.warning("You are trying to get context for a processed session. Why do you need it?")
    #     elif status == SessionStatus.PROCESSING:
    #         logger.warning("You are trying to get context for a processing session. Why do you need it?")
    #     return Context.from_api_response(response.json())

    def update(self, new_metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Update the session's metadata.

        Args:
            new_metadata: New metadata to associate with the session

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.put(
            f"/api/v1/users/{self._user_id}/sessions/{self.session_id}",
            data={"metadata": new_metadata or {}},
        )

        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self._user_id} not found" in detail:
                raise UserNotFoundError(user_id=self._user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to update session: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
        
        updated_data = SessionModel.from_api_response(response.json())
        self.metadata = updated_data.metadata

    def refresh(self) -> None:
        """
        Refresh the session data from the API.

        This method updates the local session data to reflect any changes
        that may have occurred on the server.

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
            f"/api/v1/users/{self._user_id}/sessions/{self.session_id}"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self._user_id} not found" in detail:
                raise UserNotFoundError(user_id=self._user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to refresh session: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
        
        self._session_data = SessionModel.from_api_response(response.json())
        self.status = self._session_data.status
        self.created_at = self._session_data.created_at
        self.metadata = self._session_data.metadata

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
            f"/api/v1/users/{self._user_id}/sessions/{self.session_id}/process"
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self._user_id} not found" in detail:
                raise UserNotFoundError(user_id=self._user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code == 400:
            raise InvalidSessionStateError(
                message=f"{response.json().get('detail', f'Cannot process session with status {self.status}')}."
            )
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to process session: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )

    def get_messages(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> SessionMessagesList:
        """
        Get all messages in the session.

        Returns:
            Paginated list of messages in the session

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
            f"/api/v1/users/{self._user_id}/sessions/{self.session_id}/messages",
            params={"offset": offset, "limit": limit},
        )
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self._user_id} not found" in detail:
                raise UserNotFoundError(user_id=self._user_id)
            else:
                raise SessionNotFoundError(session_id=self.session_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to get messages: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
        
        return SessionMessagesList.from_api_response(response.json())

    def __repr__(self) -> str:
        return f"<Session id={self.session_id} user_id={self._user_id} status={self.status}>"
