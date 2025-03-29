"""
User management functionality for the RecallrAI SDK.
"""

from typing import Any, Dict, Optional
from .utils import HTTPClient
from .models import User as UserModel, SessionList
from .session import Session

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
            NotFoundError: If the user is not found
            ValidationError: If the new_user_id is invalid
            BadRequestError: If a user with the new_user_id already exists
        """
        data = {}
        if new_metadata is not None:
            data["new_metadata"] = new_metadata
        if new_user_id is not None:
            data["new_user_id"] = new_user_id
            
        response = self._http.put(f"/api/v1/users/{self.user_id}", data=data)
        updated_data = UserModel.from_api_response(response)
        
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
            NotFoundError: If the user is not found
        """
        self._http.delete(f"/api/v1/users/{self.user_id}")

    def create_session(self, auto_process_after_minutes: int = -1) -> Session:
        """
        Create a new session for this user.

        Args:
            auto_process_after_minutes: Minutes to wait before auto-processing (-1 to disable)

        Returns:
            A Session object to interact with the created session

        Raises:
            ValidationError: If auto_process_after_minutes is invalid
        """
        response = self._http.post(
            f"/api/v1/users/{self.user_id}/sessions",
            data={"auto_process_after_minutes": auto_process_after_minutes},
        )
        
        session_id = response["session_id"]
        return Session(self._http, self.user_id, session_id)

    def get_session(self, session_id: str) -> Session:
        """
        Get an existing session for this user.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            A Session object to interact with the session

        Raises:
            NotFoundError: If the session is not found
        """
        return Session(self._http, self.user_id, session_id)

    def list_sessions(self, offset: int = 0, limit: int = 10) -> SessionList:
        """
        List sessions for this user with pagination.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of sessions with pagination info
        """
        response = self._http.get(
            f"/api/v1/users/{self.user_id}/sessions",
            params={"offset": offset, "limit": limit},
        )
        return SessionList.from_api_response(response)
