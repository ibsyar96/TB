from difflib import SequenceMatcher

from app.quran.normalize import tokenize

STATUS_CORRECT = "correct"
STATUS_INCORRECT = "incorrect"
STATUS_MISSED = "missed"
STATUS_EXTRA = "extra"


def align_words(expected_text: str, recited_text: str) -> list[dict]:
    expected = tokenize(expected_text)
    recited = tokenize(recited_text)

    matcher = SequenceMatcher(None, expected, recited, autojunk=False)
    result: list[dict] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        exp_chunk = expected[i1:i2]
        rec_chunk = recited[j1:j2]

        if tag == "equal":
            for word in exp_chunk:
                result.append({
                    "expected": word,
                    "heard": word,
                    "status": STATUS_CORRECT,
                })
            continue

        if tag == "replace":
            paired = min(len(exp_chunk), len(rec_chunk))
            for idx in range(paired):
                result.append({
                    "expected": exp_chunk[idx],
                    "heard": rec_chunk[idx],
                    "status": STATUS_INCORRECT,
                })
            for word in exp_chunk[paired:]:
                result.append({
                    "expected": word,
                    "heard": None,
                    "status": STATUS_MISSED,
                })
            for word in rec_chunk[paired:]:
                result.append({
                    "expected": None,
                    "heard": word,
                    "status": STATUS_EXTRA,
                })
            continue

        if tag == "delete":
            for word in exp_chunk:
                result.append({
                    "expected": word,
                    "heard": None,
                    "status": STATUS_MISSED,
                })
            continue

        if tag == "insert":
            for word in rec_chunk:
                result.append({
                    "expected": None,
                    "heard": word,
                    "status": STATUS_EXTRA,
                })

    return result


def summarize_alignment(items: list[dict], expected_word_count: int) -> dict:
    counts = {
        STATUS_CORRECT: 0,
        STATUS_INCORRECT: 0,
        STATUS_MISSED: 0,
        STATUS_EXTRA: 0,
    }
    for item in items:
        counts[item["status"]] += 1

    accuracy = (
        round((counts[STATUS_CORRECT] / expected_word_count) * 100, 1)
        if expected_word_count
        else 0.0
    )

    return {
        "accuracy_pct": accuracy,
        "counts": counts,
    }


def analyze_text(expected_text: str, recited_text: str) -> dict:
    expected_words = tokenize(expected_text)
    alignment = align_words(expected_text, recited_text)
    summary = summarize_alignment(alignment, len(expected_words))
    return {
        **summary,
        "word_alignment": alignment,
    }
