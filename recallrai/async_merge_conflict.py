"""
Async merge conflict management functionality for the RecallrAI SDK.
"""

from typing import List
from .utils.async_http_client import AsyncHTTPClient
from .models import (
    MergeConflictModel,
    MergeConflictStatus,
    MergeConflictAnswer,
)
from .exceptions import (
    UserNotFoundError,
    MergeConflictNotFoundError,
    MergeConflictAlreadyResolvedError,
    MergeConflictInvalidQuestionsError,
    MergeConflictMissingAnswersError,
    MergeConflictInvalidAnswerError,
    RecallrAIError
)
from logging import getLogger

logger = getLogger(__name__)


class AsyncMergeConflict:
    """
    Async merge conflict manager for the RecallrAI system.
    
    This class provides async methods for inspecting and resolving merge conflicts
    that occur when new memories conflict with existing ones.
    """

    def __init__(
        self,
        http_client: AsyncHTTPClient,
        user_id: str,
        conflict_data: MergeConflictModel,
    ):
        """
        Initialize an async merge conflict.

        Args:
            http_client: Async HTTP client for API communication.
            user_id: User ID who owns this conflict.
            conflict_data: Merge conflict data model.
        """
        self._http = http_client
        self.user_id = user_id
        self._conflict_data = conflict_data
        
        # Expose key properties for easy access
        self.conflict_id = conflict_data.id
        self.status = conflict_data.status
        self.new_memory_content = conflict_data.new_memory_content
        self.new_memories = conflict_data.new_memories
        self.conflicting_memories = conflict_data.conflicting_memories
        self.clarifying_questions = conflict_data.clarifying_questions
        self.created_at = conflict_data.created_at
        self.resolved_at = conflict_data.resolved_at
        self.resolution_data = conflict_data.resolution_data

    async def resolve(self, answers: List[MergeConflictAnswer]) -> None:
        """
        Resolve this merge conflict by providing answers to clarifying questions asynchronously.

        Args:
            answers: List of answers to the clarifying questions.

        Raises:
            UserNotFoundError: If the user is not found.
            MergeConflictNotFoundError: If the merge conflict is not found.
            MergeConflictAlreadyResolvedError: If the conflict is already resolved.
            MergeConflictInvalidQuestionsError: If the provided questions don't match the original questions.
            MergeConflictMissingAnswersError: If not all required questions have been answered.
            MergeConflictInvalidAnswerError: If an answer is not a valid option for its question.
            ValidationError: If the answers are invalid.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        if self.status in [MergeConflictStatus.RESOLVED, MergeConflictStatus.FAILED]:
            raise MergeConflictAlreadyResolvedError(
                message=f"Merge conflict {self.conflict_id} is already resolved",
                http_status=400
            )

        # Convert answers to the format expected by the API
        answer_data = {
            "question_answers": [
                {
                    "question": answer.question,
                    "answer": answer.answer,
                    "message": answer.message,
                }
                for answer in answers
            ]
        }

        response = await self._http.post(
            f"/api/v1/users/{self.user_id}/merge-conflicts/{self.conflict_id}/resolve",
            data={"answers": answer_data},
        )

        if response.status_code == 404:
            # Check if it's a user not found or conflict not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(message=detail, http_status=response.status_code)
            else:
                raise MergeConflictNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code == 400:
            detail = response.json().get('detail', '')
            if "already resolved" in detail:
                raise MergeConflictAlreadyResolvedError(message=detail, http_status=response.status_code)
            elif "Invalid questions provided" in detail:
                raise MergeConflictInvalidQuestionsError(
                    message=detail,
                    http_status=response.status_code
                )
            elif "Missing answers for the following questions" in detail:
                raise MergeConflictMissingAnswersError(
                    message=detail,
                    http_status=response.status_code
                )
            elif "Invalid answer" in detail and "for question" in detail:
                raise MergeConflictInvalidAnswerError(
                    message=detail,
                    http_status=response.status_code
                )
            else:
                raise RecallrAIError(
                    message=detail,
                    http_status=response.status_code
                )
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )

        # Update the conflict data with the response
        updated_data = MergeConflictModel.from_api_response(response.json())
        self._conflict_data = updated_data
        self.status = updated_data.status
        self.resolved_at = updated_data.resolved_at
        self.resolution_data = updated_data.resolution_data

    async def refresh(self) -> None:
        """
        Refresh this merge conflict's data from the API asynchronously.

        Raises:
            UserNotFoundError: If the user is not found.
            MergeConflictNotFoundError: If the merge conflict is not found.
            AuthenticationError: If the API key or project ID is invalid.
            InternalServerError: If the server encounters an error.
            NetworkError: If there are network issues.
            TimeoutError: If the request times out.
            RecallrAIError: For other API-related errors.
        """
        response = await self._http.get(
            f"/api/v1/users/{self.user_id}/merge-conflicts/{self.conflict_id}"
        )

        if response.status_code == 404:
            # Check if it's a user not found or conflict not found error
            detail = response.json().get('detail', '')
            if f"User {self.user_id} not found" in detail:
                raise UserNotFoundError(message=detail, http_status=response.status_code)
            else:
                raise MergeConflictNotFoundError(message=detail, http_status=response.status_code)
        elif response.status_code != 200:
            raise RecallrAIError(
                message=response.json().get('detail', 'Unknown error'),
                http_status=response.status_code
            )

        # Update with fresh data
        updated_data = MergeConflictModel.from_api_response(response.json())
        self._conflict_data = updated_data
        self.status = updated_data.status
        self.resolved_at = updated_data.resolved_at
        self.resolution_data = updated_data.resolution_data

    def __repr__(self) -> str:
        """Return a string representation of the async merge conflict."""
        return f"AsyncMergeConflict(id='{self.conflict_id}', status='{self.status}', user_id='{self.user_id}')"
