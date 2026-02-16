# noonapi

Official Python SDK for noon partner APIs.

This SDK currently provides:

- **Authentication / session management** using a partner credentials JSON file
- A simple **identity check** via `whoami`

More service namespaces will be added over time.

---

## Requirements

- Python **3.9+**

---

## Install

```bash
pip install noonapi
````

---

## Credentials

To use this SDK, you must first obtain partner credentials from noon.

Follow the official guide:

👉 [https://noon-docs.noonpartners.dev/docs/getting-started/getting-credentials](https://noon-docs.noonpartners.dev/docs/getting-started/getting-credentials)

You will receive a JSON credentials file. Keep this file private and do not commit it to version control.

Once you have the file, use it when creating a session:

```python
from noonapi import NoonSession

session = NoonSession("noon_credentials_sensitive.json")
```

⚠️ **Security note**

Your credentials file contains a private key. Treat it like a password:

* Do not commit it to Git.
* Do not share it publicly.
* Store it securely in production environments.

---

## Quick start (login + whoami)

```python
from noonapi import NoonSession

session = NoonSession("noon_credentials_sensitive.json")

me = session.auth.whoami()
print(me)
```

### What `NoonSession` does

* Creates a signed JWT using your credentials
* Logs in to noon Identity
* Maintains an authenticated cookie session internally
* Automatically re-authenticates and retries once if a request returns `401`

---
