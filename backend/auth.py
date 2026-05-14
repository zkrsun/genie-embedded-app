"""Auth helpers shared by all routers."""
from fastapi import Request

from config import MODE


def user_email(request: Request) -> str:
    """Resolve the calling user's email.

    Databricks Apps injects the authenticated user as `X-Forwarded-Email`.
    For local dev (MODE=LOCAL) we fall back to a fixed identity.
    """
    if MODE == "LOCAL":
        return "user@example.com"
    return request.headers.get("X-Forwarded-Email", "unknown")
