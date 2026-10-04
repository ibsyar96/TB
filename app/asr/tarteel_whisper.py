from pathlib import Path

from app.asr.base import ASRProvider

DEFAULT_MODEL_ID = "tarteel-ai/whisper-base-ar-quran"


class TarteelWhisperASR(ASRProvider):
    """Lazy-loaded Quran ASR adapter.

    The transformers dependency is intentionally optional and installed via
    requirements-worker.txt, so the text-analysis API can stay lightweight.
    """

    def __init__(self, model_id: str = DEFAULT_MODEL_ID):
        self.model_id = model_id
        self._pipe = None

    def _load(self):
        if self._pipe is not None:
            return self._pipe

        import torch
        from transformers import pipeline

        if torch.cuda.is_available():
            device = 0
        else:
            device = -1

        self._pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model_id,
            device=device,
        )
        return self._pipe

    def transcribe(self, audio_path: Path) -> str:
        pipe = self._load()
        output = pipe(
            str(audio_path),
            return_timestamps=False,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
        )
        return (output.get("text") or "").strip()
