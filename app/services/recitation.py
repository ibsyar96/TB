import asyncio
from pathlib import Path

import httpx

from app.asr.factory import describe_asr_mode, get_asr_provider
from app.persistence.supabase import get_supabase_recorder
from app.quran.data import get_ayah
from app.tahsin.matcher import analyze_text


class AyahNotAvailable(ValueError):
    pass


class EmptyTranscription(ValueError):
    pass


def analyze_transcription(
    surah: int,
    ayah: int,
    transcription: str,
    asr_mode: str = "manual-transcript",
) -> dict:
    expected = get_ayah(surah, ayah)
    if not expected:
        raise AyahNotAvailable(f"Surah {surah}, ayah {ayah} is not available")

    result = analyze_text(expected, transcription)
    return {
        "surah": surah,
        "ayah": ayah,
        "expected_text": expected,
        "transcription": transcription,
        "asr_mode": asr_mode,
        "recitation_id": None,
        "persistence_status": "not-requested",
        **result,
    }


async def analyze_audio_path(
    audio_path: Path,
    surah: int,
    ayah: int,
    *,
    telegram_user_id: int | None = None,
    telegram_username: str | None = None,
    display_name: str | None = None,
    persist: bool = True,
) -> dict:
    provider = get_asr_provider()
    transcription = await asyncio.to_thread(provider.transcribe, audio_path)

    if not transcription:
        raise EmptyTranscription("ASR returned an empty transcription")

    analysis = analyze_transcription(
        surah=surah,
        ayah=ayah,
        transcription=transcription,
        asr_mode=describe_asr_mode(),
    )

    if not persist:
        return analysis

    recorder = get_supabase_recorder()
    if recorder is None:
        analysis["persistence_status"] = "disabled"
        return analysis

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
