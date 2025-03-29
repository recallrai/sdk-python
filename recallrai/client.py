# Path: recallrai/client.py
# Description: Main client class for the RecallrAI SDK

"""
Main client class for the RecallrAI SDK.

This module provides the RecallrAI class, which is the primary interface for the SDK.
"""

import uuid
from typing import Any, Dict, Optional
from .utils import HTTPClient
from .models import User, UserList

class RecallrAI:
    """
    Main client for interacting with the RecallrAI API.
    
    This class provides methods for creating and managing users, sessions, and memories.
    """

    def __init__(
        self,
        api_key: str,
        project_id: uuid.UUID,
        base_url: str = "https://api.recallrai.com",
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
        
        self.http = HTTPClient(
            api_key=api_key,
            project_id=str(project_id),
            base_url=base_url,
            timeout=timeout,
        )
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = base_url

    # User management
    def create_user(self, user_id: str, metadata: Optional[Dict[str, Any]] = None) -> User:
        """
        Create a new user.

        Args:
            user_id: Unique identifier for the user
            metadata: Optional metadata to associate with the user

        Returns:
            The created user

        Raises:
            ValidationError: If the user_id is invalid
            BadRequestError: If a user with the same ID already exists
        """
        response = self.http.post("/api/v1/users", data={"user_id": user_id, "metadata": metadata or {}})
        return User.from_api_response(response)

    def get_user(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            The user information

        Raises:
            NotFoundError: If the user is not found
        """
        response = self.http.get(f"/api/v1/users/{user_id}")
        return User.from_api_response(response)

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
        return User.from_api_response(response)

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user.

        Args:
            user_id: ID of the user to delete

        Raises:
            NotFoundError: If the user is not found
        """
        self.http.delete(f"/api/v1/users/{user_id}")
