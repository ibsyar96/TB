from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_reports_audio_configuration():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "asr_mode" in body
    assert "persistence_configured" in body


def test_transcript_endpoint_returns_word_alignment():
    response = client.post(
        "/v1/analyze/transcript",
        json={
            "surah": 1,
            "ayah": 2,
            "transcription": "الحمد لله رب العالمين",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["accuracy_pct"] == 100.0
    assert body["counts"]["correct"] == 4
    assert body["asr_mode"] == "manual-transcript"


def test_audio_endpoint_requires_asr_configuration(monkeypatch):
    monkeypatch.delenv("TAHSIN_WORKER_URL", raising=False)
    monkeypatch.delenv("TAHSIN_LOCAL_ASR", raising=False)

    response = client.post(
        "/v1/analyze/audio",
        data={"surah": "1", "ayah": "2"},
        files={"audio": ("recitation.ogg", b"fake-audio", "audio/ogg")},
    )

    assert response.status_code == 503
