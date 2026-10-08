# Tahsin Bot

AI-assisted Quran recitation analysis for Telegram.

## Current milestone

The project now has a two-layer audio architecture:

```text
Telegram / client
      |
      v
Vercel FastAPI gateway
      |
      | raw audio
      v
Quran ASR worker
  - ffmpeg -> mono 16 kHz WAV
  - tarteel-ai/whisper-base-ar-quran
      |
      v
word-level matcher
      |
      +--> structured response
      |
      +--> optional Supabase persistence
```

The heavy Torch/Transformers model is intentionally kept out of the Vercel gateway. The gateway can call a separate worker using `TAHSIN_WORKER_URL`.

Initial reference set: **Surah Al-Fatihah**.

> Current error detection is lexical/word-level. It does not yet claim to judge makhraj, madd duration, ghunnah, qalqalah, tafkhim/tarqiq, or other acoustic tajwid features.

## API

- `GET /`
- `GET /health`
- `GET /v1/quran/1`
- `POST /v1/analyze/transcript`
- `POST /v1/analyze/audio`

### Example transcript test

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze/transcript \
  -H "Content-Type: application/json" \
  -d '{"surah":1,"ayah":2,"transcription":"الحمد لله رب العالمين"}'
```

### Example audio test

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze/audio \
  -F surah=1 \
  -F ayah=2 \
  -F audio=@recitation.ogg
```

## Run the gateway locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Without an ASR worker, transcript analysis works and the audio endpoint intentionally returns HTTP 503.

## Run the ASR worker locally

System requirement: `ffmpeg`.

```bash
pip install -r requirements-worker.txt
TAHSIN_LOCAL_ASR=1 uvicorn worker.main:app --host 0.0.0.0 --port 8001
```

Then point the gateway to it:

```bash
TAHSIN_WORKER_URL=http://127.0.0.1:8001 \
uvicorn app.main:app --reload
```

A container definition is available at `Dockerfile.worker`.

## Environment variables

Gateway:

- `TAHSIN_WORKER_URL` - ASR worker base URL
- `TAHSIN_WORKER_TOKEN` - optional shared secret for gateway -> worker
- `TAHSIN_WORKER_TIMEOUT` - defaults to 120 seconds
- `SUPABASE_URL` - optional
- `SUPABASE_SECRET_KEY` or `SUPABASE_SERVICE_ROLE_KEY` - server-only; never expose in a browser

Worker:

- `TAHSIN_ASR_MODEL` - defaults to `tarteel-ai/whisper-base-ar-quran`
- `TAHSIN_WORKER_TOKEN` - optional shared secret
- `TAHSIN_MAX_AUDIO_BYTES` - defaults to 20 MB

## Database

The Supabase schema is stored in `supabase/schema.sql`.

Tables:

- `tahsin_users`
- `recitations`
- `recitation_words`

RLS is enabled and anonymous/authenticated table access is revoked for the MVP. Writes are intended to happen only from trusted server code.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Roadmap

- M1a: text normalization + word-level matcher ✅
- M1b: audio gateway + Quran ASR worker ✅ code path
- M1c: validate with real recitation recordings
- M2: Telegram voice-message integration ✅ webhook code
- M3: reference recitation snippets
- M4: forced alignment + madd
- M5: ghunnah/qalqalah/tafkhim-tarqiq
- M6: phoneme/makhraj scoring
- M7: teacher review loop + calibration dataset


## Telegram webhook MVP

Required environment variables:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET` (recommended)

User flow:

1. Send `/tahsin 1 2`
2. Bot replies with the selected ayat
3. Reply to that bot message with a Telegram voice note
4. The bot downloads the OGG voice file, runs the Quran ASR pipeline, and replies with word-level corrections

Webhook endpoint:

`POST /telegram/webhook`

The Telegram webhook should be configured with the same secret value used in `TELEGRAM_WEBHOOK_SECRET` so incoming requests carry the `X-Telegram-Bot-Api-Secret-Token` header.

For the MVP, voice notes are limited to roughly 4 MB and the available Quran reference set is still Al-Fatihah.


## Accuracy Lab and phoneme ground truth

Tahsin Bot now separates two evidence levels:

1. **Contract benchmark** — synthetic deterministic cases that protect software behavior.
2. **Teacher-labelled audio benchmark** — real recitation recordings labelled by a qualified teacher. Only this tier can support real-world accuracy claims.

Run the contract gate:

```bash
python scripts/run_accuracy_lab.py
```

Quranic expected pronunciation is generated with `quranic-phonemizer==3.0.1` (Hafs by default), including phoneme tokens and tajweed rule IDs.

New endpoints:

- `GET /v1/quran/{surah}/{ayah}/pronunciation`
- `POST /v1/analyze/phonemes`

The phoneme endpoint is intentionally model-agnostic: a future audio phoneme recognizer can submit observed phonemes, while the same deterministic alignment layer scores substitutions, deletions, and insertions.


## CTC forced alignment

The next Tahsin layer aligns a known Quran reference against the reciter's
audio instead of trusting ASR text alone.

```text
voice / OGG
  -> ffmpeg mono 16 kHz WAV
  -> Arabic Wav2Vec2 CTC frame probabilities
  -> Viterbi forced alignment
  -> token timestamps
  -> word timestamps
  -> confidence
```

Endpoint:

- `POST /v1/align/audio` with multipart fields `surah`, `ayah`, and `audio`

The default alignment model is
`jonatasgrosman/wav2vec2-large-xlsr-53-arabic`. In the Vercel Docker path it
is baked into the image and addressed through `TAHSIN_ALIGNMENT_MODEL`.

This endpoint is an infrastructure milestone. A timestamp is not yet a Tajweed
verdict. Madd and ghunnah grading will consume these timings only after the
alignment is validated against teacher-labelled audio.
