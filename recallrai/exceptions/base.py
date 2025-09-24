"""
Base exception classes for the RecallrAI SDK.
"""

class RecallrAIError(Exception):
    """Base exception class for all RecallrAI SDK exceptions."""

    def __init__(
        self, 
        message: str, 
        http_status: int,
    ):
        """
        Initialize a RecallrAI error.

        Args:
            message: A human-readable error message.
            http_status: The HTTP status code that triggered this error.
        """
        self.message = message
        self.http_status = http_status
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return a string representation of the error."""
        return f"{self.message}. HTTP Status: {self.http_status}."
