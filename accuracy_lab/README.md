# Accuracy Lab

Accuracy Lab separates **software-contract accuracy** from **real learner-audio accuracy**.

## Tier A — contract benchmark

These are deterministic synthetic cases. They ensure that code changes do not break:

- correct / incorrect / missed / extra word detection
- phoneme substitution / deletion / insertion alignment

Passing Tier A means the software logic is behaving as expected. It does **not** prove the speech model can detect real tajwid or makhraj errors.

Run:

```bash
python scripts/run_accuracy_lab.py
```

The report is written to `accuracy_lab/latest_report.json`.

## Tier B — teacher-labelled audio benchmark

This is the metric that will determine whether Tahsin Bot is genuinely useful.

Each case should contain:

- surah and ayah
- private audio object/path
- teacher transcription
- one or more teacher-labelled errors
- optional start/end timestamps
- rule or phoneme label
- teacher notes

The database schema includes `benchmark_cases`, `benchmark_labels`, `benchmark_runs`, and `benchmark_results` for this purpose.

No production claim such as "95% accurate" should be made from Tier A. Only Tier B can support real-world accuracy claims.
