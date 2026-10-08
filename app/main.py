import asyncio
from contextlib import asynccontextmanager
import os
import tempfile
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile

from app.alignment.arabic_ctc import AlignmentModelError
from app.alignment.factory import get_ctc_aligner
from app.asr.factory import ASRNotConfigured, describe_asr_mode
from app.audio.preprocess import AudioPreprocessError, normalize_audio
from app.persistence.supabase import persistence_configured
from app.phonetics.alignment import analyze_phonemes
from app.phonetics.reference import expected_pronunciation
from app.quran.data import get_ayah, get_surah
from app.security.api_key import require_private_api_key
from app.schemas import (
    AnalysisResponse,
    ForcedAlignmentResponse,
    PhonemeAnalysisRequest,
    PhonemeAnalysisResponse,
    TranscriptAnalysisRequest,
)
from app.services.recitation import (
    AyahNotAvailable,
    EmptyTranscription,
    analyze_audio_path,
    analyze_transcription,
)
from app.telegram.router import router as telegram_router
from app.telegram.bootstrap import register_production_webhook

@asynccontextmanager
async def lifespan(app):
    app.state.telegram_webhook_status = await register_production_webhook()
    yield


app = FastAPI(
    title="Tahsin Bot API",
    version="0.5.0",
    description="Quran recitation analysis gateway and Telegram webhook.",
    lifespan=lifespan,
)

app.include_router(telegram_router)


@app.get("/")
def root():
    return {
        "name": "Tahsin Bot API",
        "version": "0.5.0",
        "docs": "/docs",
        "health": "/health",
        "telegram_webhook": "/telegram/webhook",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "milestone": "M4-ctc-forced-alignment",
        "asr_mode": describe_asr_mode(),
        "persistence_configured": persistence_configured(),
        "telegram_configured": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        "telegram_webhook_registration": getattr(
            app.state, "telegram_webhook_status", "not-attempted"
        ),
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
    _api_authorized: None = Depends(require_private_api_key),
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


@app.get("/v1/quran/{surah}/{ayah}/pronunciation")
def quran_pronunciation(surah: int, ayah: int):
    try:
        pronunciation = expected_pronunciation(surah, ayah)
    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Pronunciation reference unavailable: {exc}",
        ) from exc

    return {
        "surah": surah,
        "ayah": ayah,
        **pronunciation,
    }


@app.post("/v1/analyze/phonemes", response_model=PhonemeAnalysisResponse)
def analyze_observed_phonemes(payload: PhonemeAnalysisRequest):
    try:
        pronunciation = expected_pronunciation(payload.surah, payload.ayah)
    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Pronunciation reference unavailable: {exc}",
        ) from exc

    expected = pronunciation["phonemes"]
    analysis = analyze_phonemes(expected, payload.observed_phonemes)

    return {
        "surah": payload.surah,
        "ayah": payload.ayah,
        "reference_text": pronunciation["text"],
        "rule_ids": pronunciation["rule_ids"],
        "expected_phonemes": expected,
        "observed_phonemes": payload.observed_phonemes,
        **analysis,
    }


@app.post("/v1/align/audio", response_model=ForcedAlignmentResponse)
async def align_audio(
    surah: int = Form(...),
    ayah: int = Form(...),
    audio: UploadFile = File(...),
    _api_authorized: None = Depends(require_private_api_key),
):
    reference = get_ayah(surah, ayah)
    if not reference:
        raise HTTPException(
            status_code=404,
            detail="Ayah not available in the current MVP reference set",
        )

    suffix = Path(audio.filename or "recitation.ogg").suffix or ".ogg"
    payload = await audio.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Audio file is empty")

    with tempfile.TemporaryDirectory(prefix="tahsin-align-") as tmp:
        tmp_dir = Path(tmp)
        raw_path = tmp_dir / f"input{suffix}"
        normalized_path = tmp_dir / "normalized.wav"
        raw_path.write_bytes(payload)

        try:
            await asyncio.to_thread(
                normalize_audio,
                raw_path,
                normalized_path,
            )
        except AudioPreprocessError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        try:
            result = await asyncio.to_thread(
                get_ctc_aligner().align,
                normalized_path,
                reference,
            )
        except AlignmentModelError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "surah": surah,
        "ayah": ayah,
        **result,
    }
