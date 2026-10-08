FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/opt/huggingface
ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HUB_OFFLINE=1
ENV TAHSIN_ASR_MODEL=/opt/models/tarteel-quran-asr

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Explicit CPU wheel, not the default CUDA-enabled PyTorch dependency set.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.8.0
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Download model during build, never during a live request.
RUN HF_HUB_OFFLINE=0 python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='tarteel-ai/whisper-base-ar-quran', local_dir='/opt/models/tarteel-quran-asr', allow_patterns=['*.json','*.txt','*.model','*.bin','*.safetensors','vocab.json','merges.txt'])"

COPY main.py ./
EXPOSE 3000
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000} --workers 1"]
