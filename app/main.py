import tempfile
from pathlib import Path

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.asr.factory import ASRNotConfigured, describe_asr_mode, get_asr_provider
from app.persistence.supabase import get_supabase_recorder, persistence_configured
from app.quran.data import get_ayah, get_surah
from app.schemas import AnalysisResponse, TranscriptAnalysisRequest
from app.tahsin.matcher import analyze_text

app = FastAPI(
    title="Tahsin Bot API",
    version="0.2.0",
    description="Quran recitation analysis gateway for Tahsin Bot.",
)


def _build_analysis(
    surah: int,
    ayah: int,
    expected_text: str,
    transcription: str,
    asr_mode: str,
) -> dict:
    result = analyze_text(expected_text, transcription)
    return {
        "surah": surah,
        "ayah": ayah,
        "expected_text": expected_text,
        "transcription": transcription,
        "asr_mode": asr_mode,
        "recitation_id": None,
        "persistence_status": "not-requested",
        **result,
    }


@app.get("/")
def root():
    return {
        "name": "Tahsin Bot API",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "milestone": "M1-audio-pipeline",
        "asr_mode": describe_asr_mode(),
        "persistence_configured": persistence_configured(),
    }


@app.get("/v1/quran/{surah}")
def quran_surah(surah: int):
    data = get_surah(surah)
    if not data:
        raise HTTPException(status_code=404, detail="Surah not available in MVP")
    return {"surah": surah, **data}


@app.post("/v1/analyze/transcript", response_model=AnalysisResponse)
def analyze_transcript(payload: TranscriptAnalysisRequest):
    expected = get_ayah(payload.surah, payload.ayah)
    if not expected:
        raise HTTPException(status_code=404, detail="Ayah not available in MVP")

    return _build_analysis(
        surah=payload.surah,
        ayah=payload.ayah,
        expected_text=expected,
        transcription=payload.transcription,
        asr_mode="manual-transcript",
    )


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
    expected = get_ayah(surah, ayah)
    if not expected:
        raise HTTPException(status_code=404, detail="Ayah not available in MVP")

    try:
        provider = get_asr_provider()
    except ASRNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    suffix = Path(audio.filename or "recitation.ogg").suffix or ".ogg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await audio.read())
        temp_path = Path(temp.name)

    try:
        try:
            transcription = await run_in_threadpool(provider.transcribe, temp_path)
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"ASR worker request failed: {exc}",
            ) from exc

        if not transcription:
            raise HTTPException(
                status_code=422,
                detail="ASR returned an empty transcription",
            )

        analysis = _build_analysis(
            surah=surah,
            ayah=ayah,
            expected_text=expected,
            transcription=transcription,
            asr_mode=describe_asr_mode(),
        )

        if persist:
            recorder = get_supabase_recorder()
            if recorder is None:
                analysis["persistence_status"] = "disabled"
            else:
                try:
                    recitation_id = await recorder.save_analysis(
                        analysis=analysis,
                        asr_model=describe_asr_mode(),
                        telegram_user_id=telegram_user_id,
                        telegram_username=telegram_username,
                        display_name=display_name,
                    )
                    analysis["recitation_id"] = recitation_id
                    analysis["persistence_status"] = "saved"
                except httpx.HTTPError:
                    analysis["persistence_status"] = "failed"

        return analysis
    finally:
        temp_path.unlink(missing_ok=True)
