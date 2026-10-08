from dataclasses import dataclass


STATUS_CORRECT = "correct"
STATUS_SUBSTITUTION = "substitution"
STATUS_DELETION = "deletion"
STATUS_INSERTION = "insertion"


@dataclass(frozen=True)
class PhonemeStep:
    expected: str | None
    observed: str | None
    status: str


def align_phonemes(expected: list[str], observed: list[str]) -> list[PhonemeStep]:
    """Levenshtein alignment with explicit phoneme error operations."""
    rows = len(expected) + 1
    cols = len(observed) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            substitution_cost = 0 if expected[i - 1] == observed[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + substitution_cost,
            )

    steps: list[PhonemeStep] = []
    i, j = len(expected), len(observed)

    while i > 0 or j > 0:
        if (
            i > 0
            and j > 0
            and expected[i - 1] == observed[j - 1]
            and dp[i][j] == dp[i - 1][j - 1]
        ):
            steps.append(
                PhonemeStep(expected[i - 1], observed[j - 1], STATUS_CORRECT)
            )
            i -= 1
            j -= 1
            continue

        if (
            i > 0
            and j > 0
            and dp[i][j] == dp[i - 1][j - 1] + 1
        ):
            steps.append(
                PhonemeStep(
                    expected[i - 1],
                    observed[j - 1],
                    STATUS_SUBSTITUTION,
                )
            )
            i -= 1
            j -= 1
            continue

        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            steps.append(
                PhonemeStep(expected[i - 1], None, STATUS_DELETION)
            )
            i -= 1
            continue

        steps.append(
            PhonemeStep(None, observed[j - 1], STATUS_INSERTION)
        )
        j -= 1

    steps.reverse()
    return steps


def summarize_phoneme_alignment(steps: list[PhonemeStep]) -> dict:
    counts = {
        STATUS_CORRECT: 0,
        STATUS_SUBSTITUTION: 0,
        STATUS_DELETION: 0,
        STATUS_INSERTION: 0,
    }
    expected_total = 0

    for step in steps:
        counts[step.status] += 1
        if step.expected is not None:
            expected_total += 1

    errors = (
        counts[STATUS_SUBSTITUTION]
        + counts[STATUS_DELETION]
        + counts[STATUS_INSERTION]
    )
    accuracy = (
        round(counts[STATUS_CORRECT] / expected_total * 100, 1)
        if expected_total
        else 0.0
    )
    per = (
        round(errors / expected_total * 100, 1)
        if expected_total
        else 0.0
    )

    return {
        "accuracy_pct": accuracy,
        "phoneme_error_rate_pct": per,
        "counts": counts,
    }


def analyze_phonemes(expected: list[str], observed: list[str]) -> dict:
    steps = align_phonemes(expected, observed)
    summary = summarize_phoneme_alignment(steps)
    return {
        **summary,
        "alignment": [
            {
                "expected": step.expected,
                "observed": step.observed,
                "status": step.status,
            }
            for step in steps
        ],
    }
