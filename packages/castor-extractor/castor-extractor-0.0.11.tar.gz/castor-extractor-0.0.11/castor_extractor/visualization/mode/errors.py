from typing import Any, Optional

from .entities import ModeAnalyticsEntity


class UnexpectedApiResponseError(Exception):
    def __init__(self, resource_name: Optional[str], result: Any):
        error_msg = "Could not extract result from API response."
        error_msg += f"resource_name: {resource_name}"
        error_msg += f"result: {result}"
        super().__init__(error_msg)


class MissingPrerequisiteError(Exception):
    def __init__(
        self,
        fetched: ModeAnalyticsEntity,
        missing: ModeAnalyticsEntity,
    ):
        error_msg = f"{missing.name} must be provided to fetch {fetched.name}."
        super().__init__(error_msg)
