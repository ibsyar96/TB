from fastapi.testclient import TestClient

from app.main import app


def test_audio_endpoint_requires_key_in_production(monkeypatch):
    monkeypatch.setenv("VERCEL_ENV", "production")
    monkeypatch.setenv("TAHSIN_API_KEY", "fake-testing-secret")
    client = TestClient(app)
    response = client.post(
        "/v1/analyze/audio",
        data={"surah": "1", "ayah": "2"},
        files={"audio": ("recitation.ogg", b"test", "audio/ogg")},
    )
    assert response.status_code == 401


def test_alignment_endpoint_fails_closed_in_production(monkeypatch):
    monkeypatch.setenv("VERCEL_ENV", "production")
    monkeypatch.delenv("TAHSIN_API_KEY", raising=False)
    client = TestClient(app)
    response = client.post(
        "/v1/align/audio",
        data={"surah": "1", "ayah": "2"},
        files={"audio": ("recitation.ogg", b"test", "audio/ogg")},
    )
    assert response.status_code == 503
