from functools import lru_cache


@lru_cache(maxsize=1)
def _phonemizer():
    from quranic_phonemizer import Phonemizer

    return Phonemizer()


def _rule_id(occurrence) -> str:
    rule_id = getattr(occurrence, "rule_id", None)
    value = getattr(rule_id, "value", None)
    return str(value if value is not None else rule_id)


def expected_pronunciation(surah: int, ayah: int) -> dict:
    """Return tajweed-aware expected phonemes for a Quran ayah (Hafs)."""
    reference = f"{surah}:{ayah}"
    result = _phonemizer().analyse(reference)

    phonemes = list(result.phonemes())
    rule_ids = sorted(
        {
            rid
            for occurrence in result.rule_occurrences
            if (rid := _rule_id(occurrence)) not in {"None", ""}
        }
    )

    return {
        "reference": reference,
        "text": result.text(),
        "phonemes": phonemes,
        "rule_ids": rule_ids,
    }
