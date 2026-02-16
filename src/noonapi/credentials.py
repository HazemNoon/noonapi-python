from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class NoonCredentialsError(ValueError):
    pass


@dataclass(frozen=True)
class NoonCredentials:
    private_key: str
    key_id: str
    project_code: str

    @staticmethod
    def from_dict(d: dict[str, Any]) -> NoonCredentials:
        missing = [k for k in ("private_key", "key_id", "project_code") if not d.get(k)]
        if missing:
            raise NoonCredentialsError(f"Missing required fields in credentials JSON: {missing}")

        return NoonCredentials(
            private_key=str(d["private_key"]),
            key_id=str(d["key_id"]),
            project_code=str(d["project_code"]),
        )

    @staticmethod
    def from_file(path: str | Path) -> NoonCredentials:
        p = Path(path).expanduser()
        try:
            raw = p.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise NoonCredentialsError(f"Credentials file not found: {p}") from e

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise NoonCredentialsError(f"Credentials file is not valid JSON: {p}") from e

        if not isinstance(data, dict):
            raise NoonCredentialsError("Credentials JSON must be an object/dict at top level")

        return NoonCredentials.from_dict(data)
