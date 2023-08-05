from __future__ import annotations

from enum import Enum


class Status(str, Enum):
    """Resulting status of some action."""

    success = "success"
    failure = "failure"
    error = "error"
    skipped = "skipped"

    def __str__(self) -> str:
        return self.value

    def __add__(self, other: str) -> str:
        """Error > Failure > Success > Skipped."""
        if self == Status.error or other == Status.error:
            return Status.error

        if self == Status.failure or other == Status.failure:
            return Status.failure

        if self == Status.skipped:
            return other

        return Status.success if other == Status.success else other + self
