"""
User management functionality for the RecallrAI SDK.
"""

import json
from typing import Any, List, Dict, Optional
from .utils import HTTPClient
from .models import (
    UserModel, 
    SessionModel, 
    SessionStatus,
    SessionList, 
    UserMemoriesList, 
    UserMessagesList,
    MergeConflictList, 
    MergeConflictStatus,
    MergeConflictModel,
)
from .session import Session
from .merge_conflict import MergeConflict
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCategoriesError,
    SessionNotFoundError,
    MergeConflictNotFoundError,
    RecallrAIError
)
from logging import getLogger

logger = getLogger(__name__)

class User:
    """
    Represents a user in the RecallrAI system with methods for user management.
    
    This class wraps a user object and provides methods for updating user data,
    and for creating and managing sessions.
    """

    def __init__(
        self,
        http_client: HTTPClient,
        user_data: UserModel,
    ):
        """
        Initialize a user.

        Args:
            http_client: HTTP client for API communication.
            user_data: User data model with user information.
        """
        self._http = http_client
        self._user_data = user_data
        self.user_id = user_data.user_id
        self.metadata = user_data.metadata
        self.created_at = user_data.created_at
        self.last_active_at = user_data.last_active_at

    def update(self, new_metadata: Optional[Dict[str, Any]] = None, new_user_id: Optional[str] = None) -> None:
        """
        Update this user's metadata or ID.

        Args:
            new_metadata: New metadata to associate with the user.
            new_user_id: New ID for the user.

        Raises:
            UserNotFoundError: If the user is not found.
            UserAlreadyExistsError: If a user with the new_user_id already exists.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        data = {}
        if new_metadata is not None:
            data["new_metadata"] = new_metadata
        if new_user_id is not None:
            data["new_user_id"] = new_user_id
            
        response = self._http.put(f"/api/v1/users/{self.user_id}", data=data)
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User with ID {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code == 409:
            detail = response.json().get("detail", f"User with ID {new_user_id} already exists")
            raise UserAlreadyExistsError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
            
        updated_data = UserModel.from_api_response(response.json())
        
        # Update internal state
        self._user_data = updated_data
        self.user_id = updated_data.user_id
        self.metadata = updated_data.metadata
        self.last_active_at = updated_data.last_active_at

    def refresh(self) -> None:
        """
        Refresh this user's data from the server.
        
        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = self._http.get(f"/api/v1/users/{self.user_id}")
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User with ID {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
        
        refreshed_data = UserModel.from_api_response(response.json())
        
        # Update internal state
        self._user_data = refreshed_data
        self.user_id = refreshed_data.user_id
        self.metadata = refreshed_data.metadata
        self.created_at = refreshed_data.created_at
        self.last_active_at = refreshed_data.last_active_at

    def delete(self) -> None:
        """
        Delete this user.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = self._http.delete(f"/api/v1/users/{self.user_id}")
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User with ID {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 204:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )

    def create_session(
        self,
        auto_process_after_seconds: int = 600,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """
        Create a new session for this user.

        Args:
            auto_process_after_seconds: Seconds of inactivity allowed before automaticly processing the session (min 600).
            metadata: Optional metadata for the session.

        Returns:
            A Session object to interact with the created session.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        payload: Dict[str, Any] = {
            "auto_process_after_seconds": auto_process_after_seconds,
            "metadata": metadata or {},
        }
        response = self._http.post(
            f"/api/v1/users/{self.user_id}/sessions",
            data=payload,
        )
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 201:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
        
        session_data = SessionModel.from_api_response(response.json())
        return Session(self._http, self.user_id, session_data)

    def get_session(self, session_id: str) -> Session:
        """
        Get an existing session for this user.

        Args:
            session_id: ID of the session to retrieve.

        Returns:
            A Session object to interact with the session.

        Raises:
            UserNotFoundError: If the user is not found.
            SessionNotFoundError: If the session is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        # First, verify the session exists by fetching its details
        response = self._http.get(f"/api/v1/users/{self.user_id}/sessions/{session_id}")
        
        if response.status_code == 404:
            # Check if it's a user not found or session not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(message=detail, http_status=response.status_code)
            else:
                raise SessionNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
        
        session_data = SessionModel.from_api_response(response.json())
        return Session(self._http, self.user_id, session_data)

    def list_sessions(
        self,
        offset: int = 0,
        limit: int = 10,
        metadata_filter: Optional[Dict[str, Any]] = None,
        user_metadata_filter: Optional[Dict[str, Any]] = None,
        status_filter: Optional[List[SessionStatus]] = None,
    ) -> SessionList:
        """
        List sessions for this user with pagination.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.
            metadata_filter: Optional metadata filter for sessions.
            user_metadata_filter: Optional metadata filter for the user.
            status_filter: Optional list of session statuses to filter by (e.g., ["pending", "processing", "processed", "insufficient_balance"]).

        Returns:
            List of sessions with pagination info.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        params: Dict[str, Any] = {"offset": offset, "limit": limit}
        if metadata_filter is not None:
            params["metadata_filter"] = json.dumps(metadata_filter)
        if user_metadata_filter is not None:
            params["user_metadata_filter"] = json.dumps(user_metadata_filter)
        if status_filter is not None:
            params["status_filter"] = [status.value for status in status_filter]

        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions",
            params=params,
        )
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
            
        return SessionList.from_api_response(response.json(), self.user_id, self._http)

    def list_memories(
        self,
        offset: int = 0,
        limit: int = 20,
        categories: Optional[List[str]] = None,
        include_previous_versions: bool = True,
        include_connected_memories: bool = True,
    ) -> UserMemoriesList:
        """
        List memories for this user with optional category filters.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return (1-200).
            categories: Optional list of category names to filter by.
            include_previous_versions: Include full version history for each memory (default: True).
            include_connected_memories: Include connected memories (default: True).

        Returns:
            UserMemoriesList: Paginated list of memory items.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        params: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "include_previous_versions": include_previous_versions,
            "include_connected_memories": include_connected_memories,
        }
        if categories is not None:
            params["categories"] = categories

        response = self._http.get(
            f"/api/v1/users/{self.user_id}/memories",
            params=params,
        )

        if response.status_code == 404:
            detail = response.json().get("detail", f"User {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code == 400:
            # Backend returns 400 for invalid categories
            detail = response.json().get('detail', 'Invalid categories provided')
            raise InvalidCategoriesError(
                message=detail,
                http_status=response.status_code
            )
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code,
            )

        return UserMemoriesList.from_api_response(response.json())

    def list_merge_conflicts(
        self,
        offset: int = 0,
        limit: int = 10,
        status: Optional[MergeConflictStatus] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> MergeConflictList:
        """
        List merge conflicts for this user.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.
            status: Optional filter by conflict status.
            sort_by: Field to sort by (created_at, resolved_at).
            sort_order: Sort order (asc, desc).

        Returns:
            MergeConflictList: Paginated list of merge conflicts.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        params: Dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        if status is not None:
            params["status"] = status.value

        response = self._http.get(
            f"/api/v1/users/{self.user_id}/merge-conflicts",
            params=params,
        )

        if response.status_code == 404:
            detail = response.json().get("detail", f"User {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code,
            )

        return MergeConflictList.from_api_response(response.json(), self._http, self.user_id)

    def get_merge_conflict(self, conflict_id: str) -> MergeConflict:
        """
        Get a specific merge conflict by ID.

        Args:
            conflict_id: Unique identifier of the merge conflict.

        Returns:
            MergeConflict: The merge conflict object.

        Raises:
            UserNotFoundError: If the user is not found.
            MergeConflictNotFoundError: If the merge conflict is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/merge-conflicts/{conflict_id}"
        )

        if response.status_code == 404:
            # Check if it's a user not found or conflict not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(message=detail, http_status=response.status_code)
            else:
                raise MergeConflictNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )

        conflict_data = MergeConflictModel.from_api_response(response.json())
        return MergeConflict(self._http, self.user_id, conflict_data)

    def get_last_n_messages(self, n: int) -> UserMessagesList:
        """
        Get the last N messages for this user across all their sessions.

        This method is useful for chatbot applications where you want to see
        the recent conversation history for context.

        Args:
            n: Number of recent messages to retrieve (1-100, default: 10).

        Returns:
            UserMessagesList: List of the most recent messages.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
            ValueError: If n is not between 1 and 100.
        """
        if not (1 <= n <= 100):
            raise ValueError("n must be between 1 and 100")
        
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/messages",
            params={"limit": n}
        )
        
        if response.status_code == 404:
            detail = response.json().get("detail", f"User with ID {self.user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )
        
        return UserMessagesList.from_api_response(response.json())

    def __repr__(self) -> str:
        return f"<User id={self.user_id} created_at={self.created_at} last_active_at={self.last_active_at}>"
