import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.asr.tarteel_whisper import TarteelWhisperASR
from app.quran.data import get_ayah, get_surah
from app.schemas import AnalysisResponse, TranscriptAnalysisRequest
from app.tahsin.matcher import analyze_text

app = FastAPI(
    title="Tahsin Bot API",
    version="0.1.0",
    description="MVP Quran recitation analysis API.",
)


@app.get("/health")
def health():
    return {"status": "ok", "milestone": "M1-word-level"}


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

    result = analyze_text(expected, payload.transcription)
    return {
        "surah": payload.surah,
        "ayah": payload.ayah,
        "expected_text": expected,
        "transcription": payload.transcription,
        **result,
    }


@app.post("/v1/analyze/audio", response_model=AnalysisResponse)
async def analyze_audio(
    surah: int = Form(...),
    ayah: int = Form(...),
    audio: UploadFile = File(...),
):
    expected = get_ayah(surah, ayah)
    if not expected:
        raise HTTPException(status_code=404, detail="Ayah not available in MVP")

    suffix = Path(audio.filename or "recitation.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await audio.read())
        temp_path = Path(temp.name)

    try:
        model_id = os.getenv("TAHSIN_ASR_MODEL", "tarteel-ai/whisper-base-ar-quran")
        transcription = TarteelWhisperASR(model_id=model_id).transcribe(temp_path)
        result = analyze_text(expected, transcription)
        return {
            "surah": surah,
            "ayah": ayah,
            "expected_text": expected,
            "transcription": transcription,
            **result,
        }
    finally:
        temp_path.unlink(missing_ok=True)
