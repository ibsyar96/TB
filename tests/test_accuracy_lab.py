import json
from pathlib import Path

from app.accuracy.evaluator import evaluate_word_cases, quality_gate

ROOT = Path(__file__).resolve().parents[1]


def test_word_contract_quality_gate_passes():
    cases = json.loads(
        (ROOT / "accuracy_lab/cases/word_baseline.json").read_text(
            encoding="utf-8"
        )
    )

    report = evaluate_word_cases(cases)
    passed, failures = quality_gate(report)

    assert passed is True
    assert failures == []
    assert report["case_pass_rate"] == 1.0
    assert report["precision"] == 1.0
    assert report["recall"] == 1.0
