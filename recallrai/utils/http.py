# Path: recallrai/utils/http.py
# Description: HTTP client utilities for the RecallrAI SDK

"""
HTTP client utilities for making requests to the RecallrAI API.
"""

import json
from typing import Any, Dict, Optional, Tuple, Union

import httpx

from .exceptions import (
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    RateLimitError,
    RecallrAIError,
    ServerError,
    ValidationError,
)

ACCEPTED_STATUS_CODES = [
    200,  # OK
    201,  # Created
    204,  # No Content
]

class HTTPClient:
    """HTTP client for making requests to the RecallrAI API."""

    def __init__(
        self,
        api_key: str,
        project_id: str,
        base_url: str,
        timeout: int = 30,
    ):
        """
        Initialize the HTTP client.

        Args:
            api_key: Your RecallrAI API key
            project_id: Your project ID
            base_url: The base URL for the RecallrAI API
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(
            timeout=self.timeout,
            headers={
                "X-Api-Key": self.api_key,
                "X-Project-Id": self.project_id,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "RecallrAI-Python-SDK",
                # TODO: "SDK-Version": "0.1.0",
            },
        )

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Handle the HTTP response and raise appropriate exceptions for errors.

        Args:
            response: The HTTP response from the API

        Returns:
            The parsed JSON response body
            
        Raises:
            AuthenticationError: When the API key or project ID is invalid
            NotFoundError: When the requested resource is not found
            ValidationError: When the API rejects the request due to validation errors
            RateLimitError: When the API rate limit has been exceeded
            ServerError: When the API encounters an unexpected server error
            RecallrAIError: For other types of errors
        """
        if response.status_code == 204:
            return {}
            
        try:
            data = response.json() if response.content else {}
        except json.JSONDecodeError:
            data = {}

        error_detail = data.get("detail", "Unknown error")
        
        if response.status_code in ACCEPTED_STATUS_CODES:
            return data
        elif response.status_code == 400:
            raise BadRequestError(message=f"Bad request: {error_detail}", details=data)
        elif response.status_code == 401:
            raise AuthenticationError(message="Invalid API key or project ID", details=data)
        elif response.status_code == 404:
            raise NotFoundError(message=f"Resource not found: {error_detail}", details=data)
        elif response.status_code == 422:
            raise ValidationError(message=f"Validation error: {error_detail}", details=data)
        elif response.status_code == 429:
            raise RateLimitError(message="API rate limit exceeded", details=data)
        elif response.status_code >= 500:
            raise ServerError(message=f"Server error: {error_detail}", details=data)
        else:
            raise RecallrAIError(
                message=f"Unexpected error: {response.status_code} - {error_detail}",
                details=data,
            )

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the RecallrAI API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Query parameters
            data: Request body data

        Returns:
            The parsed JSON response
        """
        url = f"{self.base_url}{path}"
        
        # Filter out None values in params and data
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        if data:
            data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = self.client.request(
                method=method,
                url=url,
                params=params,
                json=data,
            )
            return self._handle_response(response)
        except httpx.HTTPError as e:
            raise RecallrAIError(f"HTTP error: {str(e)}")
        except Exception as e:
            raise RecallrAIError(f"Unexpected error: {str(e)}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self.request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self.request("POST", path, data=data)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return self.request("PUT", path, data=data)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self.request("DELETE", path)
