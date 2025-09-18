"""
User management functionality for the RecallrAI SDK.
"""

import json
from typing import Any, List, Dict, Optional
from .utils import HTTPClient
from .models import UserModel, SessionList, UserMemoriesList
from .session import Session
from .exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    SessionNotFoundError,
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
            http_client: HTTP client for API communication
            user_data: User data model with user information
        """
        self._http = http_client
        self._user_data = user_data
        self.user_id = user_data.user_id
        self.metadata = user_data.metadata
        self.created_at = user_data.created_at
        self.last_active_at = user_data.last_active_at

    def update(self, new_metadata: Optional[Dict[str, Any]] = None, new_user_id: Optional[str] = None) -> 'User':
        """
        Update this user's metadata or ID.

        Args:
            new_metadata: New metadata to associate with the user
            new_user_id: New ID for the user

        Returns:
            The updated user object

        Raises:
            UserNotFoundError: If the user is not found
            UserAlreadyExistsError: If a user with the new_user_id already exists
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        data = {}
        if new_metadata is not None:
            data["metadata"] = new_metadata
        if new_user_id is not None:
            data["new_user_id"] = new_user_id
            
        response = self._http.put(f"/api/v1/users/{self.user_id}", data=data)
        
        if response.status_code == 404:
            raise UserNotFoundError(user_id=self.user_id)
        elif response.status_code == 409:
            raise UserAlreadyExistsError(user_id=new_user_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to update user: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
            
        updated_data = UserModel.from_api_response(response.json())
        
        # Update internal state
        self._user_data = updated_data
        self.user_id = updated_data.user_id
        self.metadata = updated_data.metadata
        self.last_active_at = updated_data.last_active_at
        
        return self

    def delete(self) -> None:
        """
        Delete this user.

        Raises:
            UserNotFoundError: If the user is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self._http.delete(f"/api/v1/users/{self.user_id}")
        
        if response.status_code == 404:
            raise UserNotFoundError(user_id=self.user_id)
        elif response.status_code != 204:
            raise RecallrAIError(
                message=f"Failed to delete user: {response.json().get('detail', 'Unknown error')}",
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
            auto_process_after_seconds: Seconds to wait before auto-processing (min 600)
            metadata: Optional metadata for the session

        Returns:
            A Session object to interact with the created session

        Raises:
            UserNotFoundError: If the user is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
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
            raise UserNotFoundError(user_id=self.user_id)
        elif response.status_code != 201:
            raise RecallrAIError(
                message=f"Failed to create session: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
        
        session_id = response.json()["session_id"]
        return Session(self._http, self.user_id, session_id)

    def get_session(self, session_id: str) -> Session:
        """
        Get an existing session for this user.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            A Session object to interact with the session

        Raises:
            UserNotFoundError: If the user is not found
            SessionNotFoundError: If the session is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        # Verify the session exists by checking its status
        session = Session(self._http, self.user_id, session_id)
        try:
            session.get_status()  # This will raise appropriate errors if the session doesn't exist
            return session
        except SessionNotFoundError:
            raise
        except Exception as e:
            raise RecallrAIError(f"Error retrieving session: {str(e)}")

    def list_sessions(
        self,
        offset: int = 0,
        limit: int = 10,
        metadata_filter: Optional[Dict[str, Any]] = None,
        user_metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> SessionList:
        """
        List sessions for this user with pagination.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of sessions with pagination info

        Raises:
            UserNotFoundError: If the user is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        params: Dict[str, Any] = {"offset": offset, "limit": limit}
        if metadata_filter is not None:
            params["metadata_filter"] = json.dumps(metadata_filter)
        if user_metadata_filter is not None:
            params["user_metadata_filter"] = json.dumps(user_metadata_filter)

        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions",
            params=params,
        )
        
        if response.status_code == 404:
            raise UserNotFoundError(user_id=self.user_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to list sessions: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code
            )
            
        return SessionList.from_api_response(response.json())

    def list_memories(
        self,
        offset: int = 0,
        limit: int = 20,
        categories: Optional[List[str]] = None,
    ) -> UserMemoriesList:
        """
        List memories for this user with optional category filters.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return
            categories: Optional list of category names to filter by

        Returns:
            UserMemoriesList: Paginated list of memory items

        Raises:
            UserNotFoundError: If the user is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        params: Dict[str, Any] = {"offset": offset, "limit": limit}
        if categories is not None:
            params["categories"] = categories

        response = self._http.get(
            f"/api/v1/users/{self.user_id}/memories",
            params=params,
        )

        if response.status_code == 404:
            raise UserNotFoundError(user_id=self.user_id)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=f"Failed to list memories: {response.json().get('detail', 'Unknown error')}",
                http_status=response.status_code,
            )

        return UserMemoriesList.from_api_response(response.json())
