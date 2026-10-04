import re
import unicodedata

# Arabic harakat + Qur'anic annotation marks.
_ARABIC_MARKS_RE = re.compile(
    "[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]"
)
_NON_ARABIC_RE = re.compile(r"[^\u0621-\u063A\u0641-\u064A\s]")
_SPACE_RE = re.compile(r"\s+")

_NORMALIZE_MAP = str.maketrans({
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ٱ": "ا",
    "ى": "ي",
    "ؤ": "و",
    "ئ": "ي",
    "ـ": "",
})


def normalize_arabic(text: str) -> str:
    """Normalize Arabic for ASR/text comparison, not for tajwid judgement."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_NORMALIZE_MAP)
    text = _ARABIC_MARKS_RE.sub("", text)
    text = _NON_ARABIC_RE.sub(" ", text)
    return _SPACE_RE.sub(" ", text).strip()


def tokenize(text: str) -> list[str]:
    normalized = normalize_arabic(text)
    return normalized.split() if normalized else []
