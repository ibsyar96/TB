from fastapi.testclient import TestClient

from asr_service.main import _require_worker_token, app

client = TestClient(app)


def test_health_does_not_expose_secrets(monkeypatch):
    monkeypatch.setenv("TAHSIN_WORKER_TOKEN", "PRIVATE_TEST_ONLY")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "tahsin-asr"
    assert "PRIVATE_TEST_ONLY" not in response.text


def test_worker_fails_closed_without_token(monkeypatch):
    monkeypatch.delenv("TAHSIN_WORKER_TOKEN", raising=False)
    response = client.post(
        "/v1/transcribe",
        files={"audio": ("test.ogg", b"hello", "audio/ogg")},
    )
    assert response.status_code == 503


def test_worker_rejects_invalid_token_before_audio_processing(monkeypatch):
    monkeypatch.setenv("TAHSIN_WORKER_TOKEN", "correct-private-token")
    response = client.post(
        "/v1/transcribe",
        headers={"X-Worker-Token": "wrong"},
        files={"audio": ("test.ogg", b"hello", "audio/ogg")},
    )
    assert response.status_code == 401


def test_worker_accepts_valid_token_with_stubbed_inference(monkeypatch):
    import asr_service.main as worker

    monkeypatch.setenv("TAHSIN_WORKER_TOKEN", "correct-private-token")
    monkeypatch.setattr(worker, "_normalize_audio", lambda source, dest: dest.write_bytes(b"RIFF"))
    monkeypatch.setattr(worker, "_duration_seconds", lambda path: 5.1)
    monkeypatch.setattr(worker, "_transcribe", lambda path: "الحمد لله رب العالمين")

    response = client.post(
        "/v1/transcribe",
        headers={"X-Worker-Token": "correct-private-token"},
        files={"audio": ("voice.ogg", b"voice-audio", "audio/ogg")},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "الحمد لله رب العالمين"
    assert response.json()["audio_duration_seconds"] == 5.1
