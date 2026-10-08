from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from threading import Lock

from app.alignment.viterbi import CTCAlignmentError, ctc_viterbi_align
from app.quran.normalize import normalize_arabic

DEFAULT_ALIGNMENT_MODEL = "jonatasgrosman/wav2vec2-large-xlsr-53-arabic"


class AlignmentModelError(RuntimeError):
    pass


@dataclass(frozen=True)
class TimedToken:
    token: str
    token_id: int
    start_ms: float
    end_ms: float
    confidence: float


@dataclass(frozen=True)
class TimedWord:
    text: str
    start_ms: float
    end_ms: float
    confidence: float


class ArabicCTCAligner:
    def __init__(self, model_id: str = DEFAULT_ALIGNMENT_MODEL):
        self.model_id = model_id
        self._processor = None
        self._model = None
        self._device = None
        self._load_lock = Lock()

    def _load(self):
        if self._processor is not None and self._model is not None:
            return self._processor, self._model, self._device

        with self._load_lock:
            if self._processor is not None and self._model is not None:
                return self._processor, self._model, self._device

            import torch
            from transformers import AutoModelForCTC, AutoProcessor

            processor = AutoProcessor.from_pretrained(self.model_id)
            model = AutoModelForCTC.from_pretrained(self.model_id)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model.to(device)
            model.eval()

            self._processor = processor
            self._model = model
            self._device = device

        return self._processor, self._model, self._device

    @staticmethod
    def _mono_float32(audio_path: Path) -> tuple:
        import numpy as np
        import soundfile as sf

        samples, sample_rate = sf.read(
            str(audio_path),
            dtype="float32",
            always_2d=False,
        )
        if getattr(samples, "ndim", 1) > 1:
            samples = np.mean(samples, axis=1, dtype=np.float32)
        samples = np.asarray(samples, dtype=np.float32)
        return samples, int(sample_rate)

    @staticmethod
    def _group_words(
        token_segments: list[TimedToken],
        reference_words: list[str],
        delimiter: str | None,
    ) -> list[TimedWord]:
        if not token_segments:
            return []

        groups: list[list[TimedToken]] = []
        current: list[TimedToken] = []

        for segment in token_segments:
            if delimiter and segment.token == delimiter:
                if current:
                    groups.append(current)
                    current = []
                continue
            current.append(segment)

        if current:
            groups.append(current)

        words: list[TimedWord] = []
        for index, group in enumerate(groups):
            text = (
                reference_words[index]
                if index < len(reference_words)
                else "".join(item.token for item in group)
            )
            duration_weights = [
                max(item.end_ms - item.start_ms, 1.0)
                for item in group
            ]
            weight_total = sum(duration_weights)
            confidence = sum(
                item.confidence * weight
                for item, weight in zip(group, duration_weights)
            ) / weight_total

            words.append(
                TimedWord(
                    text=text,
                    start_ms=round(group[0].start_ms, 2),
                    end_ms=round(group[-1].end_ms, 2),
                    confidence=round(float(confidence), 6),
                )
            )

        return words

    def align(self, audio_path: Path, reference_text: str) -> dict:
        import torch

        processor, model, device = self._load()
        tokenizer = processor.tokenizer

        normalized_reference = normalize_arabic(reference_text)
        if not normalized_reference:
            raise AlignmentModelError("Reference text became empty after normalization")

        encoded = tokenizer(
            normalized_reference,
            add_special_tokens=False,
        )
        token_ids = list(encoded["input_ids"])
        if not token_ids:
            raise AlignmentModelError("Alignment tokenizer produced no tokens")

        unk_token_id = tokenizer.unk_token_id
        if unk_token_id is not None and unk_token_id in token_ids:
            tokens = tokenizer.convert_ids_to_tokens(token_ids)
            raise AlignmentModelError(
                f"Reference contains token(s) unknown to alignment model: {tokens}"
            )

        samples, sample_rate = self._mono_float32(audio_path)
        if sample_rate != 16000:
            raise AlignmentModelError(
                f"Alignment requires 16000 Hz audio, got {sample_rate} Hz"
            )
        if samples.size == 0:
            raise AlignmentModelError("Audio is empty")

        inputs = processor(
            samples,
            sampling_rate=16000,
            return_tensors="pt",
        )
        input_values = inputs.input_values.to(device)

        with torch.inference_mode():
            logits = model(input_values).logits[0]
            log_probs = torch.log_softmax(logits, dim=-1).detach().cpu().numpy()

        blank_id = getattr(model.config, "pad_token_id", None)
        if blank_id is None:
            blank_id = tokenizer.pad_token_id
        if blank_id is None:
            blank_id = 0

        try:
            alignment = ctc_viterbi_align(
                log_probs,
                token_ids,
                int(blank_id),
            )
        except CTCAlignmentError as exc:
            raise AlignmentModelError(str(exc)) from exc

        audio_duration_ms = float(samples.size / sample_rate * 1000.0)
        frame_duration_ms = audio_duration_ms / max(len(log_probs), 1)
        token_labels = tokenizer.convert_ids_to_tokens(token_ids)

        timed_tokens = [
            TimedToken(
                token=str(token_labels[item.token_index]),
                token_id=item.token_id,
                start_ms=round(item.start_frame * frame_duration_ms, 2),
                end_ms=round(item.end_frame * frame_duration_ms, 2),
                confidence=item.confidence,
            )
            for item in alignment.token_segments
        ]

        delimiter = getattr(tokenizer, "word_delimiter_token", None)
        timed_words = self._group_words(
            timed_tokens,
            normalized_reference.split(),
            delimiter,
        )
        non_delimiter_tokens = [
            token
            for token in timed_tokens
            if not delimiter or token.token != delimiter
        ]
        overall_confidence = (
            sum(token.confidence for token in non_delimiter_tokens)
            / len(non_delimiter_tokens)
            if non_delimiter_tokens
            else 0.0
        )

        return {
            "model_id": self.model_id,
            "reference_text": reference_text,
            "normalized_reference": normalized_reference,
            "sample_rate_hz": sample_rate,
            "audio_duration_ms": round(audio_duration_ms, 2),
            "ctc_frame_duration_ms": round(frame_duration_ms, 4),
            "path_score": round(alignment.path_score, 4),
            "confidence": round(float(overall_confidence), 6),
            "tokens": [
                {
                    "token": item.token,
                    "token_id": item.token_id,
                    "start_ms": item.start_ms,
                    "end_ms": item.end_ms,
                    "confidence": item.confidence,
                }
                for item in timed_tokens
            ],
            "words": [
                {
                    "text": item.text,
                    "start_ms": item.start_ms,
                    "end_ms": item.end_ms,
                    "confidence": item.confidence,
                }
                for item in timed_words
            ],
        }
