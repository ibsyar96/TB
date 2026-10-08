# Quran-specific Whisper ASR Worker

The Vercel project **tahsin-asr-worker** should use:

- Git repository: `ibsyar96/TB`
- Root directory: `asr_service`
- Framework: Container/Docker (auto-detect `Dockerfile.vercel`)

Vercel env (Production only): `TAHSIN_WORKER_TOKEN`.

The model `tarteel-ai/whisper-base-ar-quran` is baked into the image during
deployment; it is not pulled in production. The model's license is Apache 2.0.

The API is protected by a shared token and must never be called from
untrusted clients with the token embedded in browser code:

```text
POST /v1/transcribe
X-Worker-Token: <server-only shared secret>
multipart/form-data:
  audio: <ogg/wav/mp3>
```

Gateway Vercel env variables:

- `TAHSIN_WORKER_URL`: production worker origin
- `TAHSIN_WORKER_TOKEN`: the same shared secret

The gateway already has a `RemoteASRProvider` adapter and needs no new
ASR dependency itself.

The worker is **CPU inference**. This has cost and latency implications;
Telegram audio should be limited to short ayat for the MVP. Future
milestones should use a persistent GPU inference service, durable task
queue, and teacher-labelled quality metrics.

A successful worker health check proves HTTP and process setup, **not**
Quran recitation accuracy.
