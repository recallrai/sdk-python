# Path: recallrai/client.py
# Description: Main client class for the RecallrAI SDK

"""
Main client class for the RecallrAI SDK.

This module provides the RecallrAI class, which is the primary interface for the SDK.
"""

import uuid
from typing import Any, Dict, Optional
from pydantic import HttpUrl
from .models import User as UserModel, UserList, SessionStatus, SessionList
from .user import User
from .session import Session
from .utils import HTTPClient
from logging import getLogger

logger = getLogger(__name__)

class RecallrAI:
    """
    Main client for interacting with the RecallrAI API.
    
    This class provides methods for creating and managing users, sessions, and memories.
    """

    def __init__(
        self,
        api_key: str,
        project_id: uuid.UUID,
        base_url: HttpUrl = "https://api.recallrai.com",
        timeout: int = 30,
    ):
        """
        Initialize the RecallrAI client.

        Args:
            api_key: Your RecallrAI API key
            project_id: Your project ID
            base_url: The base URL for the RecallrAI API
            timeout: Request timeout in seconds
        """
        if not api_key.startswith("rai_"):
            raise ValueError("API key must start with 'rai_'")
        
        self.api_key = api_key
        self.project_id = str(project_id)
        self.base_url = str(base_url)
        
        self.http = HTTPClient(
            api_key=self.api_key,
            project_id=self.project_id,
            base_url=self.base_url,
            timeout=timeout,
        )

    # User management
    def create_user(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> User:
        """
        Create a new user.

        Args:
            user_id: Unique identifier for the user
            metadata: Optional metadata to associate with the user

        Returns:
            The created user object

        Raises:
            ValidationError: If the user_id is invalid
            BadRequestError: If a user with the same ID already exists
        """
        response = self.http.post("/api/v1/users", data={"user_id": user_id, "metadata": metadata or {}})
        user_data = UserModel.from_api_response(response)
        return User(self.http, user_data)

    def get_user(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            A User object representing the user

        Raises:
            NotFoundError: If the user is not found
        """
        response = self.http.get(f"/api/v1/users/{user_id}")
        user_data = UserModel.from_api_response(response)
        return User(self.http, user_data)

    def list_users(self, offset: int = 0, limit: int = 10) -> UserList:
        """
        List users with pagination.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users with pagination info
        """
        response = self.http.get("/api/v1/users", params={"offset": offset, "limit": limit})
        return UserList.from_api_response(response)

    def update_user(
        self, 
        user_id: str, 
        new_metadata: Optional[Dict[str, Any]] = None, 
        new_user_id: Optional[str] = None
    ) -> User:
        """
        Update a user's metadata or ID.

        Args:
            user_id: Current ID of the user
            new_metadata: New metadata to associate with the user
            new_user_id: New ID for the user

        Returns:
            The updated user

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
            
        response = self.http.put(f"/api/v1/users/{user_id}", data=data)
        user_data = UserModel.from_api_response(response)
        return User(self.http, user_data)

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user.

        Args:
            user_id: ID of the user to delete

        Raises:
            NotFoundError: If the user is not found
        """
        self.http.delete(f"/api/v1/users/{user_id}")

    # Session management
    def create_session(self, user_id: str, auto_process_after_minutes: int = -1) -> Session:
        """
        Create a new session for a user.

        Args:
            user_id: ID of the user to create the session for
            auto_process_after_minutes: Minutes to wait before auto-processing (-1 to disable)

        Returns:
            A Session object to interact with the created session

        Raises:
            NotFoundError: If the user is not found
            ValidationError: If auto_process_after_minutes is invalid
        """
        response = self.http.post(
            f"/api/v1/users/{user_id}/sessions",
            data={"auto_process_after_minutes": auto_process_after_minutes},
        )
        
        session_id = response["session_id"]
        return Session(self.http, user_id, session_id)

    def get_session(self, user_id: str, session_id: str) -> Session:
        """
        Get an existing session.

        Args:
            user_id: ID of the user who owns the session
            session_id: ID of the session to retrieve

        Returns:
            A Session object to interact with the session

        Raises:
            NotFoundError: If the user or session is not found
        """
        # Ensure the session exists by checking its status
        session = Session(self.http, user_id, session_id)
        status = session.get_status()
        if status == SessionStatus.PROCESSING:
            raise RecallrAIError("Session is already processing. You can't add messages to it. Create a new session instead.")
        elif status == SessionStatus.PROCESSED:
            raise RecallrAIError("Session has already been processed. You can't add messages to it. Create a new session instead.")
        
        return session

    def list_sessions(self, user_id: str, offset: int = 0, limit: int = 10) -> SessionList:
        """
        List sessions for a user with pagination.

        Args:
            user_id: ID of the user
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of sessions with pagination info

        Raises:
            NotFoundError: If the user is not found
        """
        response = self.http.get(
            f"/api/v1/users/{user_id}/sessions",
            params={"offset": offset, "limit": limit},
        )
        return SessionList.from_api_response(response)
