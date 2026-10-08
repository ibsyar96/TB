"""Register the production Telegram webhook without exporting the bot token.

Only executes during the Vercel production app lifespan. A failed Telegram
request never blocks the app from serving and does not log the token-bearing URL.
"""
import logging
import os
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)


def webhook_configuration() -> tuple[str, str, str] | None:
    if os.getenv("VERCEL_ENV") != "production":
        return None
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
    url = os.getenv("TELEGRAM_WEBHOOK_URL")
    if not token or not secret or not url:
        return None
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path != "/telegram/webhook"
    ):
        raise ValueError("Invalid Telegram webhook URL configuration")
    if not 1 <= len(secret) <= 256:
        raise ValueError("Invalid Telegram webhook secret length")
    return token, secret, url


async def register_production_webhook() -> str:
    config = webhook_configuration()
    if config is None:
        return "not-configured"

    token, secret, url = config
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{token}/setWebhook",
                json={
                    "url": url,
                    "secret_token": secret,
                    "allowed_updates": ["message"],
                    "drop_pending_updates": False,
                    "max_connections": 4,
                },
            )
            response.raise_for_status()
            payload = response.json()
        if payload.get("ok") is True and payload.get("result") is True:
            logger.info("Production Telegram webhook registered")
            return "registered"
        logger.warning("Telegram webhook registration rejected")
        return "rejected"
    except (httpx.HTTPError, ValueError) as exc:
        # Never log str(exc): httpx exceptions may contain the bot token in URL.
        logger.warning(
            "Telegram webhook registration failed (%s)",
            type(exc).__name__,
        )
        return "failed"
