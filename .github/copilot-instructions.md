# Copilot PR Review Instructions — Noon API SDK
This file guides Copilot when adding or updating SDK service files from synced swagger definitions.

Primary reference:
- Use `src/noonapi/services/auth.py` as the baseline example for structure, style, imports, naming, and error handling.

Repository file responsibilities:
- `src/noonapi/session.py`
  - Root SDK entrypoint.
  - Owns the shared `requests.Session`.
  - Owns authentication lifecycle and retry-on-401 behavior through `NoonSession.request(...)`.
  - Only expose a new service here if that service file is actually being added.
- `src/noonapi/services/auth.py`
  - Existing hand-written reference implementation.
  - Do not modify unless explicitly requested.
  - New services should mirror this file's simplicity and style.
- `src/noonapi/services/__init__.py`
  - Export service classes that actually exist.
  - Do not add imports for services that have not been added.
- `src/noonapi/constants.py`
  - Keep shared gateway URLs and endpoint URL helpers here when a constant is truly shared.
  - Do not move service-specific logic here.
- `src/noonapi/errors.py`
  - Keep the current SDK error model unchanged unless explicitly requested.
- `openapi/swagger/`
  - Swagger source of truth for endpoints, request shapes, and response shapes.
  - Swagger is also the source of truth for URL construction, including base path and versioned route segments such as `/fbpi/v1/...`.
  - Use swagger as input, but do not let it force a code structure that conflicts with the SDK style.
- `scripts/sync_swagger.sh`
  - Only for syncing swagger assets.
  - Do not turn this into a service-code generator pipeline unless explicitly requested.

Rules for adding a new service file such as `fbpi`, `pricing`, or `stock`:
- Add the service under `src/noonapi/services/<service>.py`.
- Follow the same constructor pattern as `auth.py` where possible.
- Keep methods explicit and readable.
- Prefer small hand-written wrappers over generic abstractions.
- Use `NoonSession.request(...)` for outbound requests so retry behavior remains centralized.
- Reuse the existing `NoonApiError` behavior and the current response-handling style.
- Match the current SDK style for docstrings, imports, typing, and method naming.
- Keep changes minimal and scoped to the service being added.

What not to add:
- No new generation frameworks.
- No helper runtimes or service registries.
- No mixin-based service attachment systems.
- No auto-generated `_generated.py`-style indirection.
- No extra GitHub Actions or CI/CD workflows just for service generation.
- No broad refactors unrelated to the requested service.
- No additional dependencies.

Expected change set when adding a service:
- Add `src/noonapi/services/<service>.py`.
- Update `src/noonapi/services/__init__.py`.
- Update `src/noonapi/session.py` if the new service should be exposed as `session.<service>`.
- Only touch `src/noonapi/constants.py` if a shared endpoint helper is genuinely needed.

Swagger usage instructions:
- Read the synced swagger file for the target service.
- Use it to determine HTTP methods, full endpoint paths, base path, version segments, required headers, path params, query params, and request bodies.
- Build request URLs from the swagger-defined path shape for that service.
- Do not guess or invent service URL prefixes manually.
- Convert that information into SDK code that matches the existing codebase rather than mirroring swagger mechanically.
- If swagger and current SDK style conflict, prioritize the existing SDK style and keep the wrapper readable.

Core constraint:
- The goal is for Copilot-assisted service code to look like it belongs in this repository already, with `auth.py` as the example, and without introducing parallel infrastructure.
