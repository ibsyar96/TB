import os
import tempfile
from pathlib import Path

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.asr.factory import ASRNotConfigured, describe_asr_mode
from app.persistence.supabase import persistence_configured
from app.quran.data import get_surah
from app.schemas import AnalysisResponse, TranscriptAnalysisRequest
from app.services.recitation import (
    AyahNotAvailable,
    EmptyTranscription,
    analyze_audio_path,
    analyze_transcription,
)
from app.telegram.router import router as telegram_router

app = FastAPI(
    title="Tahsin Bot API",
    version="0.3.0",
    description="Quran recitation analysis gateway and Telegram webhook.",
)

app.include_router(telegram_router)


@app.get("/")
def root():
    return {
        "name": "Tahsin Bot API",
        "version": "0.3.0",
        "docs": "/docs",
        "health": "/health",
        "telegram_webhook": "/telegram/webhook",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "milestone": "M2-telegram-webhook",
        "asr_mode": describe_asr_mode(),
        "persistence_configured": persistence_configured(),
        "telegram_configured": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }


@app.get("/v1/quran/{surah}")
def quran_surah(surah: int):
    data = get_surah(surah)
    if not data:
        raise HTTPException(status_code=404, detail="Surah not available in MVP")
    return {"surah": surah, **data}


@app.post("/v1/analyze/transcript", response_model=AnalysisResponse)
def analyze_transcript(payload: TranscriptAnalysisRequest):
    try:
        return analyze_transcription(
            surah=payload.surah,
            ayah=payload.ayah,
            transcription=payload.transcription,
        )
    except AyahNotAvailable as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/v1/analyze/audio", response_model=AnalysisResponse)
async def analyze_audio(
    surah: int = Form(...),
    ayah: int = Form(...),
    audio: UploadFile = File(...),
    telegram_user_id: int | None = Form(default=None),
    telegram_username: str | None = Form(default=None),
    display_name: str | None = Form(default=None),
    persist: bool = Form(default=True),
):
    suffix = Path(audio.filename or "recitation.ogg").suffix or ".ogg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await audio.read())
        temp_path = Path(temp.name)

    try:
        try:
            return await analyze_audio_path(
                temp_path,
                surah=surah,
                ayah=ayah,
                telegram_user_id=telegram_user_id,
                telegram_username=telegram_username,
                display_name=display_name,
                persist=persist,
            )
        except AyahNotAvailable as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ASRNotConfigured as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except EmptyTranscription as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"ASR worker request failed: {exc}",
            ) from exc
    finally:
        temp_path.unlink(missing_ok=True)
