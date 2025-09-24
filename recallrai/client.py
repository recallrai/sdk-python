"""
Main client class for the RecallrAI SDK.

This module provides the RecallrAI class, which is the primary interface for the SDK.
"""

import json
from typing import Any, Dict, Optional
from .models import UserModel, UserList
from .user import User
from .utils import HTTPClient
from .exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    RecallrAIError,
)
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
        project_id: str,
        base_url: str = "https://api.recallrai.com",
        timeout: int = 30,
    ):
        """
        Initialize the RecallrAI client.

        Args:
            api_key: Your RecallrAI API key.
            project_id: Your project ID.
            base_url: The base URL for the RecallrAI API.
            timeout: Request timeout in seconds.
        """
        if not api_key.startswith("rai_"):
            raise ValueError("API key must start with 'rai_'")
        
        self._http = HTTPClient(
            api_key=api_key,
            project_id=project_id,
            base_url=base_url,
            timeout=timeout,
        )

    # User management
    def create_user(
        self, 
        user_id: str, 
        metadata: Optional[Dict[str, Any]] = None,
    ) -> User:
        """
        Create a new user.

        Args:
            user_id: Unique identifier for the user.
            metadata: Optional metadata to associate with the user.

        Returns:
            The created user object.

        Raises:
            UserAlreadyExistsError: If a user with the same ID already exists.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = self._http.post("/api/v1/users", data={"user_id": user_id, "metadata": metadata or {}})
        if response.status_code == 409:
            detail = response.json().get("detail", f"User with ID {user_id} already exists")
            raise UserAlreadyExistsError(message=detail, http_status=response.status_code)
        elif response.status_code != 201:
            detail = response.json().get("detail", "Failed to create user")
            raise RecallrAIError(message=detail, http_status=response.status_code)
        user_data = UserModel.from_api_response(response.json())
        return User(self._http, user_data)

    def get_user(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            A User object representing the user.

        Raises:
            UserNotFoundError: If the user is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = self._http.get(f"/api/v1/users/{user_id}")
        if response.status_code == 404:
            detail = response.json().get("detail", f"User with ID {user_id} not found")
            raise UserNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            detail = response.json().get("detail", "Failed to retrieve user")
            raise RecallrAIError(message=detail, http_status=response.status_code)
        user_data = UserModel.from_api_response(response.json())
        return User(self._http, user_data)

    def list_users(
        self, 
        offset: int = 0, 
        limit: int = 10, 
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> UserList:
        """
        List users with pagination.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of users with pagination info.
        
        Raises:
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        params: Dict[str, Any] = {"offset": offset, "limit": limit}
        if metadata_filter is not None:
            params["metadata_filter"] = json.dumps(metadata_filter)

        response = self._http.get("/api/v1/users", params=params)
        if response.status_code != 200:
            detail = response.json().get("detail", "Failed to list users")
            raise RecallrAIError(message=detail, http_status=response.status_code)
        return UserList.from_api_response(response.json(), self._http)
