from __future__ import annotations

from typing import Any, Optional


class NoonApiError(Exception):
    """
    Error returned by noon APIs.

    Attributes:
      - http_status: standard HTTP status code (e.g. 401, 403, 500)
      - status_code: platform error code string returned in the response body
      - status_id: platform error code integer returned in the response body
      - details: optional list with extra error context
    """

    def __init__(
        self,
        *,
        http_status: int,
        message: str,
        status_code: Optional[str] = None,
        status_id: Optional[int] = None,
        details: Optional[list[Any]] = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.status_code = status_code
        self.status_id = status_id
        self.details = details or []
