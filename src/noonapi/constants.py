NOON_GATEWAY_BASE_URL = "https://noon-api-gateway.noon.partners"


def url(path: str) -> str:
    """
    Join noon gateway base url with an absolute path like:
      /identity/v1/whoami
    """
    if not path.startswith("/"):
        path = "/" + path
    return NOON_GATEWAY_BASE_URL + path


# Identity
def identity_login_url() -> str:
    return url("/identity/public/v1/api/login")


def identity_whoami_url() -> str:
    return url("/identity/v1/whoami")
