"""
HTTP client for making requests to the RecallrAI API.
"""
from httpx import Response, Client, TimeoutException, NetworkError, ConnectError
from typing import Any, Dict, Optional
from ..exceptions import (
    TimeoutError, 
    ConnectionError,
    ValidationError,
    InternalServerError,
    AuthenticationError,
)

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
        self.client = Client(
            timeout=self.timeout,
            headers={
                "X-Api-Key": self.api_key,
                "X-Project-Id": self.project_id,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"RecallrAI-Python-SDK/0.2.0",
            },
        )

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Response:
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
            if response.status_code == 422:
                raise ValidationError(
                    details=response.json()["detail"],
                )
            elif response.status_code == 500:
                raise InternalServerError(
                    details=response.json()["detail"],
                )
            elif response.status_code == 401:
                raise AuthenticationError(
                    details=response.json()["detail"],
                )
            
            return response
        except TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except ConnectError as e:
            raise ConnectionError(f"Failed to connect to the API: {e}")
        except Exception as e:
            # Handle other exceptions as needed
            raise e

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Response:
        """Make a GET request."""
        return self.request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """Make a POST request."""
        return self.request("POST", path, data=data)

    def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Response:
        """Make a PUT request."""
        return self.request("PUT", path, data=data)

    def delete(self, path: str) -> Response:
        """Make a DELETE request."""
        return self.request("DELETE", path)
