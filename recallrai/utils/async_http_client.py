"""
Async HTTP client for making requests to the RecallrAI API.
"""

from json import JSONDecodeError
from httpx import Response, AsyncClient, TimeoutException, ConnectError, Limits
from typing import Any, Dict, Optional
from ..exceptions import (
    TimeoutError, 
    ConnectionError,
    ValidationError,
    InternalServerError,
    AuthenticationError,
)


class AsyncHTTPClient:
    """Async HTTP client for making requests to the RecallrAI API."""

    def __init__(
        self,
        api_key: str,
        project_id: str,
        base_url: str,
        timeout: int = 30,
    ):
        """
        Initialize the async HTTP client.

        Args:
            api_key: Your RecallrAI API key.
            project_id: Your project ID.
            base_url: The base URL for the RecallrAI API.
            timeout: Request timeout in seconds.
        """

        self.api_key = api_key
        self.project_id = project_id
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        # Configure connection limits to handle concurrent requests better
        # Default httpx limits can cause connection errors under high concurrency
        limits = Limits(
            max_connections=100,  # Maximum total connections
            max_keepalive_connections=20,  # Maximum idle connections to keep alive
        )
        
        self._client = AsyncClient(
            timeout=self.timeout,
            limits=limits,
            headers={
                "X-Recallr-Api-Key": self.api_key,
                "X-Recallr-Project-Id": self.project_id,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"RecallrAI-Python-SDK/0.3.2",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _ensure_client(self):
        """Ensure the client is initialized."""
        if self._client is None:
            # Configure connection limits to handle concurrent requests better
            limits = Limits(
                max_connections=100,
                max_keepalive_connections=20,
            )
            
            self._client = AsyncClient(
                timeout=self.timeout,
                limits=limits,
                headers={
                    "X-Recallr-Api-Key": self.api_key,
                    "X-Recallr-Project-Id": self.project_id,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": f"RecallrAI-Python-SDK/0.3.2",
                },
            )

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Make an async request to the RecallrAI API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            params: Query parameters.
            data: Request body data.

        Returns:
            The parsed JSON response.
        """
        await self._ensure_client()
        
        url = f"{self.base_url}{path}"
        
        # Filter out None values in params and data
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        if data:
            data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = await self._client.request(  # type: ignore
                method=method,
                url=url,
                params=params,
                json=data,
            )
            
            if response.status_code == 204:
                return response  # No content to parse
            
            elif response.status_code == 422:
                detail = response.json().get("detail", "Validation error")
                raise ValidationError(
                    message=detail,
                    http_status=response.status_code
                )
            elif response.status_code == 500:
                detail = response.json().get("detail", "Internal server error")
                raise InternalServerError(
                    message=detail,
                    http_status=response.status_code
                )
            elif response.status_code == 401:
                detail = response.json().get("detail", "Authentication failed")
                raise AuthenticationError(
                    message=detail,
                    http_status=response.status_code
                )
            
            # Try to parse to JSON to catch JSON errors early
            _ = response.json()
            
            return response
        except TimeoutException as e:
            raise TimeoutError(
                message=f"Request timed out: {e}",
                http_status=0  # No HTTP status for timeout
            )
        except (ConnectError, JSONDecodeError) as e:
            raise ConnectionError(
                message=f"Failed to connect to the API: {e}",
                http_status=0  # No HTTP status for connection error
            )
        except Exception as e:
            # Handle other exceptions as needed
            raise e

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Response:
        """Make an async GET request."""
        return await self.request("GET", path, params=params)

    async def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """Make an async POST request."""
        return await self.request("POST", path, data=data)

    async def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """Make an async PUT request."""
        return await self.request("PUT", path, data=data)

    async def delete(self, path: str) -> Response:
        """Make an async DELETE request."""
        return await self.request("DELETE", path)

    async def close(self):
        """Close the async client."""
        if self._client:
            await self._client.aclose()
            self._client = None
