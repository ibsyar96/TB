from pydantic import BaseModel, Field


class TranscriptAnalysisRequest(BaseModel):
    surah: int = Field(ge=1, le=114)
    ayah: int = Field(ge=1)
    transcription: str = Field(min_length=1)


class WordAlignment(BaseModel):
    expected: str | None
    heard: str | None
    status: str


class AnalysisResponse(BaseModel):
    surah: int
    ayah: int
    expected_text: str
    transcription: str
    asr_mode: str
    recitation_id: str | None = None
    persistence_status: str
    accuracy_pct: float
    counts: dict[str, int]
    word_alignment: list[WordAlignment]
