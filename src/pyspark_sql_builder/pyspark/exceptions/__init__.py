"""PySpark SQL Builder exceptions module.

Mirrors PySpark's exception API for compatibility.
"""

from __future__ import annotations


class AnalysisExceptionError(Exception):
    """Exception raised for analysis errors matching PySpark's AnalysisException.

    This exception is raised when there are issues analyzing a SQL query,
    such as referencing non-existent tables or invalid column references.

    Mirrors: pyspark.errors.exceptions.captured.AnalysisException
    """

    def __init__(self, message: str, error_class: str | None = None) -> None:
        """Initialize AnalysisExceptionError.

        Args:
            message: The error message.
            error_class: Optional error class identifier (e.g.,
                "TABLE_OR_VIEW_NOT_FOUND").
        """
        super().__init__(message)
        self.message = message
        self.error_class = error_class


__all__ = ["AnalysisExceptionError"]
