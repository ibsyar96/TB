import asyncio

from app.telegram.bootstrap import webhook_configuration, register_production_webhook


def test_bootstrap_is_disabled_outside_production(monkeypatch):
    monkeypatch.setenv("VERCEL_ENV", "preview")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "sample")
    monkeypatch.setenv("TELEGRAM_WEBHOOK_SECRET", "example-secret")
    monkeypatch.setenv(
        "TELEGRAM_WEBHOOK_URL",
        "https://tahsinbot1.vercel.app/telegram/webhook",
    )
    assert webhook_configuration() is None
    assert asyncio.run(register_production_webhook()) == "not-configured"


def test_bootstrap_requires_valid_https_webhook(monkeypatch):
    monkeypatch.setenv("VERCEL_ENV", "production")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "sample")
    monkeypatch.setenv("TELEGRAM_WEBHOOK_SECRET", "example-secret")
    monkeypatch.setenv(
        "TELEGRAM_WEBHOOK_URL",
        "http://example.org/telegram/webhook",
    )
    import pytest

    with pytest.raises(ValueError, match="Invalid Telegram webhook URL"):
        webhook_configuration()


def test_webhook_registration_uses_secret_without_leaking_it(monkeypatch):
    import httpx

    monkeypatch.setenv("VERCEL_ENV", "production")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:TEST_BOT_TOKEN")
    monkeypatch.setenv("TELEGRAM_WEBHOOK_SECRET", "secret-for-test")
    monkeypatch.setenv(
        "TELEGRAM_WEBHOOK_URL",
        "https://tahsinbot1.vercel.app/telegram/webhook",
    )

    seen = []

    def respond(request):
        seen.append(request)
        assert request.method == "POST"
        assert request.url.path.endswith("/setWebhook")
        import json

        body = json.loads(request.content)
        assert body["secret_token"] == "secret-for-test"
        assert body["url"] == "https://tahsinbot1.vercel.app/telegram/webhook"
        return httpx.Response(200, json={"ok": True, "result": True})

    real_async_client = httpx.AsyncClient

    def fake_client(*args, **kwargs):
        return real_async_client(transport=httpx.MockTransport(respond), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", fake_client)

    result = asyncio.run(register_production_webhook())
    assert result == "registered"
    assert len(seen) == 1
