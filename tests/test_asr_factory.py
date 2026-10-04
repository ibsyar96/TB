import pytest

from app.asr.factory import ASRNotConfigured, describe_asr_mode, get_asr_provider
from app.asr.remote import RemoteASRProvider


def test_asr_is_unconfigured_by_default(monkeypatch):
    monkeypatch.delenv("TAHSIN_WORKER_URL", raising=False)
    monkeypatch.delenv("TAHSIN_LOCAL_ASR", raising=False)

    assert describe_asr_mode() == "unconfigured"
    with pytest.raises(ASRNotConfigured):
        get_asr_provider()


def test_remote_worker_is_preferred(monkeypatch):
    monkeypatch.setenv("TAHSIN_WORKER_URL", "https://worker.example.com")
    monkeypatch.delenv("TAHSIN_LOCAL_ASR", raising=False)

    provider = get_asr_provider()

    assert describe_asr_mode() == "remote-worker"
    assert isinstance(provider, RemoteASRProvider)
