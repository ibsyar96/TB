# Tahsin Bot

AI-assisted Quran recitation analysis for Telegram.

## Milestone 1

The first milestone is intentionally narrow:

1. User selects a known Quran verse.
2. Audio is transcribed with a Quran-specific ASR adapter.
3. The transcription is normalized and aligned word-by-word with the canonical verse.
4. The API returns structured JSON: correct, incorrect, missed, and extra words.

Initial reference set: **Surah Al-Fatihah**.

> This milestone detects lexical/word-level recitation errors. It does **not** yet claim to judge makhraj, madd duration, ghunnah, qalqalah, or other acoustic tajwid features.

## Architecture

```text
Audio
  -> Quran ASR adapter
  -> Arabic normalization
  -> word alignment
  -> analysis JSON
```

The ASR layer is deliberately replaceable. The initial worker adapter targets `tarteel-ai/whisper-base-ar-quran`, while later milestones can add forced alignment and tajwid-aware phoneme/acoustic analysis.

## API

- `GET /health`
- `GET /v1/quran/1`
- `POST /v1/analyze/transcript`
- `POST /v1/analyze/audio`

## Local quick start

Core/API:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

For real audio ASR:

```bash
pip install -r requirements-worker.txt
```

The ASR model is loaded lazily only when the audio endpoint is used.

## Example transcript analysis

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze/transcript \
  -H "Content-Type: application/json" \
  -d '{"surah":1,"ayah":2,"transcription":"الحمد لله رب العالمين"}'
```

## Roadmap

- M1: Quran ASR + word-level error JSON
- M2: Telegram voice-message integration
- M3: reference recitation snippets
- M4: forced alignment + madd
- M5: ghunnah/qalqalah/tafkhim-tarqiq
- M6: phoneme/makhraj scoring
- M7: teacher review loop + calibration dataset
