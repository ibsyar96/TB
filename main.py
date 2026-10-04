# Vercel FastAPI entrypoint.
# The heavy Quran ASR model lives in worker/main.py and is called remotely.
from app.main import app
