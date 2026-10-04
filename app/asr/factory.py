import os

from app.asr.base import ASRProvider
from app.asr.remote import RemoteASRProvider
from app.asr.tarteel_whisper import TarteelWhisperASR


class ASRNotConfigured(RuntimeError):
    pass


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def describe_asr_mode() -> str:
    if os.getenv("TAHSIN_WORKER_URL"):
        return "remote-worker"
    if _truthy(os.getenv("TAHSIN_LOCAL_ASR")):
        return "local-tarteel"
    return "unconfigured"


def get_asr_provider() -> ASRProvider:
    worker_url = os.getenv("TAHSIN_WORKER_URL")
    if worker_url:
        return RemoteASRProvider(
            worker_url=worker_url,
            worker_token=os.getenv("TAHSIN_WORKER_TOKEN"),
            timeout_seconds=float(os.getenv("TAHSIN_WORKER_TIMEOUT", "120")),
        )

    if _truthy(os.getenv("TAHSIN_LOCAL_ASR")):
        model_id = os.getenv(
            "TAHSIN_ASR_MODEL",
            "tarteel-ai/whisper-base-ar-quran",
        )
        return TarteelWhisperASR(model_id=model_id)

    raise ASRNotConfigured(
        "Audio ASR is not configured. Set TAHSIN_WORKER_URL or TAHSIN_LOCAL_ASR=1."
    )
