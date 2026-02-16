from pathlib import Path

from noonapi import NoonSession

HERE = Path(__file__).resolve().parent
CREDS_PATH = HERE / "noon_credentials_sensitive.json"

session = NoonSession(str(CREDS_PATH))

me = session.auth.whoami()
print("whoami:", me)
