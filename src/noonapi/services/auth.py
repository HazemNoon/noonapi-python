from __future__ import annotations

import time
import uuid
from typing import Any

import jwt
import requests

from ..constants import identity_login_url, identity_whoami_url
from ..credentials import NoonCredentials
from ..errors import NoonApiError


class AuthService:
    """
    Authentication service (PRD).
    - Creates a signed token (RS256) from partner credentials
    - Logs in via Identity login endpoint (cookie-based session)
    - Exposes whoami for identity verification
    """

    def __init__(
        self,
        http: requests.Session,
        credentials: NoonCredentials,
        *,
        timeout_s: float,
        verify_whoami_on_login: bool,
    ) -> None:
        self._http = http
        self._credentials = credentials
        self._timeout_s = timeout_s
        self._verify_whoami_on_login = verify_whoami_on_login

    def _create_token(self) -> str:
        payload = {
            "sub": self._credentials.key_id,
            "iat": int(time.time()),
            "jti": str(uuid.uuid4()),
        }

        token = jwt.encode(payload, self._credentials.private_key, algorithm="RS256")
        return token.decode("utf-8") if isinstance(token, bytes) else token

    def login(self) -> None:
        res = self._http.post(
            identity_login_url(),
            json={
                "token": self._create_token(),
                "default_project_code": self._credentials.project_code,
            },
            timeout=self._timeout_s,
        )
        self._raise_for_error(res)

        if self._verify_whoami_on_login:
            self.whoami()

    def refresh(self) -> None:
        self.login()

    def whoami(self) -> dict[str, Any]:
        res = self._http.get(identity_whoami_url(), timeout=self._timeout_s)
        self._raise_for_error(res)

        data = res.json()
        if not isinstance(data, dict):
            raise NoonApiError(http_status=200, message=f"Unexpected whoami response: {type(data)}")

        return data

    @staticmethod
    def _raise_for_error(res: requests.Response) -> None:
        if res.status_code < 400:
            return

        http_status = res.status_code

        try:
            data = res.json()
        except Exception as err:
            raise NoonApiError(http_status=http_status, message=res.text) from err

        if isinstance(data, dict):
            message = data.get("message") or res.text
            details = data.get("details")
            raise NoonApiError(
                http_status=http_status,
                message=str(message),
                status_code=data.get("status_code"),
                status_id=data.get("status_id"),
                details=details if isinstance(details, list) else None,
            )

        raise NoonApiError(http_status=http_status, message=str(data))
