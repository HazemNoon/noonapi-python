from __future__ import annotations

from typing import Any

import requests

from .credentials import NoonCredentials
from .services.auth import AuthService


class NoonSession:
    """
    Root SDK entrypoint.

    Owns:
      - partner credentials
      - auto re-auth + retry-once behavior on HTTP 401
      - auth namespace: session.auth.*
    """

    def __init__(
        self,
        credentials_path: str,
        *,
        user_agent: str = "NoonApiClient/1.0",
        timeout_s: float = 30.0,
        auto_login: bool = True,
        verify_whoami_on_login: bool = True,
    ) -> None:
        """
        Create a new authenticated noon session.

        Args:
            credentials_path:
                Path to the partner credentials JSON file obtained from noon.
            user_agent:
                Value to send in the `User-Agent` header for all outgoing requests.
            timeout_s:
                Default timeout (in seconds) applied to all HTTP requests.
            auto_login:
                If True, performs login immediately during session creation.
                If False, login must be triggered manually via `session.auth.login()`.
            verify_whoami_on_login:
                If True, performs a `whoami` call immediately after login to verify
                that the session is authenticated correctly.
        """
        self.timeout_s = timeout_s

        self.credentials = NoonCredentials.from_file(credentials_path)

        self._http = requests.Session()
        self._http.headers.update({"User-Agent": user_agent})

        self.auto_login = auto_login
        self.auth = AuthService(
            self._http,
            self.credentials,
            timeout_s=self.timeout_s,
            verify_whoami_on_login=verify_whoami_on_login,
        )

        if self.auto_login:
            self.auth.login()

    @property
    def http(self) -> requests.Session:
        """
        Access the underlying `requests.Session`.

        This is primarily intended for advanced usage.
        """
        return self._http

    def request(
        self, method: str, url: str, *, retry_on_401: bool = True, **kwargs: Any
    ) -> requests.Response:
        """
        Send an HTTP request using the authenticated session.

        Automatically refreshes authentication once if a 401 response is received.

        Args:
            method:
                HTTP method (e.g. "GET", "POST", "PUT", "DELETE").
            url:
                Absolute URL to call.
            retry_on_401:
                If True, automatically re-authenticates and retries once when
                a 401 Unauthorized response is returned.
            **kwargs:
                Additional arguments forwarded directly to `requests.Session.request`.

        Returns:
            The `requests.Response` object.
        """
        res = self._http.request(method, url, timeout=self.timeout_s, **kwargs)

        if retry_on_401 and res.status_code == 401:
            self.auth.refresh()
            res = self._http.request(method, url, timeout=self.timeout_s, **kwargs)

        return res
