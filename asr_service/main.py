"""Isolated Quran ASR worker.

ASR inference is intentionally separated from the Telegram gateway because
the torch/transformers runtime is too heavy for its native FastAPI bundle.
"""
from __future__ import annotations

import asyncio
import hmac
import os
import subprocess
import tempfile
import threading
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile

MODEL_PATH = os.getenv("TAHSIN_ASR_MODEL", "/opt/models/tarteel-quran-asr")
MAX_AUDIO_BYTES = int(os.getenv("TAHSIN_MAX_AUDIO_BYTES", "4000000"))
MAX_AUDIO_SECONDS = float(os.getenv("TAHSIN_MAX_AUDIO_SECONDS", "40"))
_MODEL = None
_MODEL_LOCK = threading.Lock()

app = FastAPI(
    title="Tahsin Quran ASR Worker",
    version="0.1.0",
    description="Private audio transcription for the Tahsin Telegram gateway.",
)


def _require_worker_token(received: str | None) -> None:
    expected = os.getenv("TAHSIN_WORKER_TOKEN", "")
    if not expected:
        # Fail closed even on Preview: a public worker must never run costly
        # inference without its own shared secret.
        raise HTTPException(status_code=503, detail="Worker token not configured")
    if received is None or not hmac.compare_digest(received, expected):
        raise HTTPException(status_code=401, detail="Invalid worker token")


def _normalize_audio(source: Path, destination: Path) -> None:
    command = [
        "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
        "-y", "-i", str(source), "-vn",
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(destination),
    ]
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("Could not preprocess audio") from None
    if process.returncode != 0:
        raise ValueError("Invalid or unsupported audio") from None
    if not destination.is_file() or destination.stat().st_size < 48:
        raise ValueError("Audio conversion produced no usable samples")


def _duration_seconds(wav_path: Path) -> float:
    import wave
    try:
        with wave.open(str(wav_path), "rb") as stream:
            return stream.getnframes() / stream.getframerate()
    except (OSError, EOFError, wave.Error, ZeroDivisionError):
        raise ValueError("Audio WAV could not be decoded") from None


def _get_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    with _MODEL_LOCK:
        if _MODEL is not None:
            return _MODEL
        import torch
        from transformers import pipeline
        torch.set_num_threads(max(1, min(os.cpu_count() or 2, 2)))
        _MODEL = pipeline(
            task="automatic-speech-recognition",
            model=MODEL_PATH,
            device="cpu",
        )
        return _MODEL


def _transcribe(wav_path: Path) -> str:
    model = _get_model()
    output = model(str(wav_path), return_timestamps=False)
    return str(output.get("text") or "").strip()


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "tahsin-asr",
        "model_loaded": _MODEL is not None,
    }


@app.post("/v1/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    x_worker_token: str | None = Header(default=None),
):
    _require_worker_token(x_worker_token)
    # Telegram voice notes are normally OGG/Opus.
    if not audio.filename:
        raise HTTPException(status_code=400, detail="Filename required")

    with tempfile.TemporaryDirectory(prefix="quran-asr-") as temp_dir:
        directory = Path(temp_dir)
        input_path = directory / "input_audio"
        normalized_path = directory / "audio_16k.wav"

        total = 0
        with input_path.open("wb") as output:
            while True:
                chunk = await audio.read(1024 * 256)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_AUDIO_BYTES:
                    raise HTTPException(status_code=413, detail="Audio file too large")
                output.write(chunk)
        if not total:
            raise HTTPException(status_code=400, detail="Empty audio")

        try:
            await asyncio.to_thread(_normalize_audio, input_path, normalized_path)
            seconds = await asyncio.to_thread(_duration_seconds, normalized_path)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        if seconds > MAX_AUDIO_SECONDS:
            raise HTTPException(
                status_code=413,
                detail="Recording too long for current Tahsin MVP",
            )
        text = await asyncio.to_thread(_transcribe, normalized_path)

    if not text:
        raise HTTPException(status_code=422, detail="ASR returned no transcription")
    return {
        "text": text,
        "model_id": "tarteel-ai/whisper-base-ar-quran",
        "audio_duration_seconds": round(seconds, 2),
    }
