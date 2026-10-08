import json
from pathlib import Path

from app.accuracy.evaluator import evaluate_word_cases, quality_gate
from app.phonetics.alignment import analyze_phonemes

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run_phoneme_contract(cases: list[dict]) -> dict:
    results = []
    passed = 0

    for case in cases:
        analysis = analyze_phonemes(case["expected"], case["observed"])
        ok = analysis["counts"] == case["expected_counts"]
        passed += int(ok)
        results.append(
            {
                "id": case["id"],
                "passed": ok,
                "counts": analysis["counts"],
                "expected_counts": case["expected_counts"],
            }
        )

    total = len(cases)
    return {
        "evidence_level": "contract-synthetic",
        "total_cases": total,
        "passed_cases": passed,
        "case_pass_rate": round(passed / total, 4) if total else 0.0,
        "cases": results,
    }


def main() -> int:
    word_cases = load_json("accuracy_lab/cases/word_baseline.json")
    phoneme_cases = load_json("accuracy_lab/cases/phoneme_contract.json")

    word_report = evaluate_word_cases(word_cases)
    phoneme_report = run_phoneme_contract(phoneme_cases)

    word_ok, failures = quality_gate(word_report)
    phoneme_ok = phoneme_report["case_pass_rate"] == 1.0
    if not phoneme_ok:
        failures.append("phoneme contract pass rate must be 100%")

    report = {
        "status": "pass" if word_ok and phoneme_ok else "fail",
        "word_error": word_report,
        "phoneme_contract": phoneme_report,
        "failures": failures,
        "note": (
            "Synthetic contract tests protect software behavior. "
            "They are not evidence of real learner-audio accuracy."
        ),
    }

    output = ROOT / "accuracy_lab" / "latest_report.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
