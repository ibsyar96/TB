import hmac
import os

from fastapi import Header, HTTPException


def require_private_api_key(
    x_tahsin_api_key: str | None = Header(default=None),
) -> None:
    """Protect compute-intensive endpoints when published on a public domain.

    Production fails closed if no server-only API key has been configured.
    """
    expected = os.getenv("TAHSIN_API_KEY")
    if not expected:
        if os.getenv("VERCEL_ENV") == "production":
            raise HTTPException(
                status_code=503,
                detail="Private analysis API is not configured",
            )
        return
    if not x_tahsin_api_key or not hmac.compare_digest(
        x_tahsin_api_key, expected
    ):
        raise HTTPException(
            status_code=401, detail="Private analysis API key required"
        )
