import os
from functools import lru_cache

from app.alignment.arabic_ctc import ArabicCTCAligner, DEFAULT_ALIGNMENT_MODEL


@lru_cache(maxsize=1)
def get_ctc_aligner() -> ArabicCTCAligner:
    model_id = os.getenv("TAHSIN_ALIGNMENT_MODEL", DEFAULT_ALIGNMENT_MODEL)
    return ArabicCTCAligner(model_id=model_id)
