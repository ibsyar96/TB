from dataclasses import dataclass

from app.services.recitation import analyze_transcription


@dataclass(frozen=True)
class DetectionMetrics:
    true_positive: int
    false_positive: int
    false_negative: int

    @property
    def precision(self) -> float:
        denominator = self.true_positive + self.false_positive
        return self.true_positive / denominator if denominator else 1.0

    @property
    def recall(self) -> float:
        denominator = self.true_positive + self.false_negative
        return self.true_positive / denominator if denominator else 1.0

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        return 2 * p * r / (p + r) if p + r else 0.0


def _event_key(event: dict) -> tuple:
    return (
        event.get("status"),
        event.get("expected"),
        event.get("heard"),
    )


def predicted_word_errors(analysis: dict) -> set[tuple]:
    return {
        _event_key(item)
        for item in analysis["word_alignment"]
        if item["status"] != "correct"
    }


def expected_word_errors(case: dict) -> set[tuple]:
    return {
        _event_key(item)
        for item in case.get("expected_errors", [])
    }


def evaluate_word_cases(cases: list[dict]) -> dict:
    tp = fp = fn = passed = 0
    case_results = []

    for case in cases:
        analysis = analyze_transcription(
            surah=case["surah"],
            ayah=case["ayah"],
            transcription=case["transcription"],
        )
        predicted = predicted_word_errors(analysis)
        expected = expected_word_errors(case)

        case_tp = len(predicted & expected)
        case_fp = len(predicted - expected)
        case_fn = len(expected - predicted)
        case_passed = predicted == expected

        tp += case_tp
        fp += case_fp
        fn += case_fn
        passed += int(case_passed)

        case_results.append(
            {
                "id": case["id"],
                "passed": case_passed,
                "predicted_errors": sorted(predicted),
                "expected_errors": sorted(expected),
            }
        )

    metrics = DetectionMetrics(tp, fp, fn)
    total = len(cases)
    return {
        "evidence_level": "contract-synthetic",
        "total_cases": total,
        "passed_cases": passed,
        "case_pass_rate": round(passed / total, 4) if total else 0.0,
        "precision": round(metrics.precision, 4),
        "recall": round(metrics.recall, 4),
        "f1": round(metrics.f1, 4),
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
        "cases": case_results,
    }


def quality_gate(report: dict) -> tuple[bool, list[str]]:
    failures: list[str] = []

    if report["case_pass_rate"] < 1.0:
        failures.append("word benchmark case pass rate must be 100%")
    if report["precision"] < 1.0:
        failures.append("word benchmark precision must be 100%")
    if report["recall"] < 1.0:
        failures.append("word benchmark recall must be 100%")

    return not failures, failures
