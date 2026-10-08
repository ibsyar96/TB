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


class PhonemeAnalysisRequest(BaseModel):
    surah: int = Field(ge=1, le=114)
    ayah: int = Field(ge=1)
    observed_phonemes: list[str] = Field(min_length=1)


class PhonemeAlignmentItem(BaseModel):
    expected: str | None
    observed: str | None
    status: str


class PhonemeAnalysisResponse(BaseModel):
    surah: int
    ayah: int
    reference_text: str
    rule_ids: list[str]
    expected_phonemes: list[str]
    observed_phonemes: list[str]
    accuracy_pct: float
    phoneme_error_rate_pct: float
    counts: dict[str, int]
    alignment: list[PhonemeAlignmentItem]


class AlignmentToken(BaseModel):
    token: str
    token_id: int
    start_ms: float
    end_ms: float
    confidence: float


class AlignmentWord(BaseModel):
    text: str
    start_ms: float
    end_ms: float
    confidence: float


class ForcedAlignmentResponse(BaseModel):
    surah: int
    ayah: int
    model_id: str
    reference_text: str
    normalized_reference: str
    sample_rate_hz: int
    audio_duration_ms: float
    ctc_frame_duration_ms: float
    path_score: float
    confidence: float
    tokens: list[AlignmentToken]
    words: list[AlignmentWord]
