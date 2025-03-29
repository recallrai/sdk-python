"""
Main client class for the RecallrAI SDK.

This module provides the RecallrAI class, which is the primary interface for the SDK.
"""

from typing import Any, Dict, Optional
from .models import User as UserModel, UserList
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
            api_key: Your RecallrAI API key
            project_id: Your project ID
            base_url: The base URL for the RecallrAI API
            timeout: Request timeout in seconds
        """
        if not api_key.startswith("rai_"):
            raise ValueError("API key must start with 'rai_'")
        
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = base_url
        
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
            UserAlreadyExistsError: If a user with the same ID already exists
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self.http.post("/api/v1/users", data={"user_id": user_id, "metadata": metadata or {}})
        if response.status_code == 409:
            raise UserAlreadyExistsError(user_id=user_id)
        elif response.status_code != 201:
            raise RecallrAIError("Failed to create user", http_status=response.status_code)
        user_data = UserModel.from_api_response(response.json())
        return User(self.http, user_data)

    def get_user(self, user_id: str) -> User:
        """
        Get a user by ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            A User object representing the user

        Raises:
            UserNotFoundError: If the user is not found
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self.http.get(f"/api/v1/users/{user_id}")
        if response.status_code == 404:
            raise UserNotFoundError(user_id=user_id)
        elif response.status_code != 200:
            raise RecallrAIError("Failed to retrieve user", http_status=response.status_code)
        user_data = UserModel.from_api_response(response.json())
        return User(self.http, user_data)

    def list_users(self, offset: int = 0, limit: int = 10) -> UserList:
        """
        List users with pagination.

        Args:
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of users with pagination info
        
        Raises:
            AuthenticationError: If the API key or project ID is invalid
            InternalServerError: If the server encounters an error
            NetworkError: If there are network issues
            TimeoutError: If the request times out
            RecallrAIError: For other API-related errors
        """
        response = self.http.get("/api/v1/users", params={"offset": offset, "limit": limit})
        if response.status_code != 200:
            raise RecallrAIError("Failed to list users", http_status=response.status_code)
        return UserList.from_api_response(response.json())
