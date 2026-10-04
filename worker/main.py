import hmac
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.audio.preprocess import AudioPreprocessError, ffmpeg_available, normalize_audio
from app.asr.tarteel_whisper import DEFAULT_MODEL_ID, TarteelWhisperASR

MAX_AUDIO_BYTES = int(os.getenv("TAHSIN_MAX_AUDIO_BYTES", str(20 * 1024 * 1024)))
MODEL_ID = os.getenv("TAHSIN_ASR_MODEL", DEFAULT_MODEL_ID)

app = FastAPI(
    title="Tahsin ASR Worker",
    version="0.1.0",
    description="Heavy Quran ASR worker for Tahsin Bot.",
)

_asr = TarteelWhisperASR(model_id=MODEL_ID)


def _verify_worker_token(token: str | None) -> None:
    expected = os.getenv("TAHSIN_WORKER_TOKEN")
    if not expected:
        return
    if not token or not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="Invalid worker token")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_id": MODEL_ID,
        "ffmpeg": ffmpeg_available(),
    }


@app.post("/v1/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    x_worker_token: str | None = Header(default=None),
):
    _verify_worker_token(x_worker_token)

    payload = await audio.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Audio file is empty")
    if len(payload) > MAX_AUDIO_BYTES:
        raise HTTPException(status_code=413, detail="Audio file is too large")

    suffix = Path(audio.filename or "recitation.ogg").suffix or ".ogg"
    with tempfile.TemporaryDirectory(prefix="tahsin-asr-") as tmp:
        tmp_dir = Path(tmp)
        input_path = tmp_dir / f"input{suffix}"
        normalized_path = tmp_dir / "normalized.wav"
        input_path.write_bytes(payload)

        try:
            await run_in_threadpool(
                normalize_audio,
                input_path,
                normalized_path,
            )
        except AudioPreprocessError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        text = await run_in_threadpool(_asr.transcribe, normalized_path)

    return {
        "text": text,
        "model_id": MODEL_ID,
        "sample_rate_hz": 16000,
        "channels": 1,
    }
