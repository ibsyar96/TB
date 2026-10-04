import os
from pathlib import Path

import httpx

from app.asr.base import ASRProvider


class RemoteASRProvider(ASRProvider):
    def __init__(
        self,
        worker_url: str,
        worker_token: str | None = None,
        timeout_seconds: float = 120.0,
    ):
        self.worker_url = worker_url.rstrip("/")
        self.worker_token = worker_token
        self.timeout_seconds = timeout_seconds

    def transcribe(self, audio_path: Path) -> str:
        headers = {}
        if self.worker_token:
            headers["X-Worker-Token"] = self.worker_token

        with audio_path.open("rb") as handle:
            files = {
                "audio": (
                    audio_path.name,
                    handle,
                    "application/octet-stream",
                )
            }
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(
                    f"{self.worker_url}/v1/transcribe",
                    headers=headers,
                    files=files,
                )
                response.raise_for_status()
                payload = response.json()

        return (payload.get("text") or "").strip()
