from app.telegram.formatting import (
    extract_reference,
    format_analysis,
)


def test_extract_reference_from_bot_prompt():
    assert extract_reference("Balas voice note\nRef: 1:2") == (1, 2)


def test_format_analysis_shows_incorrect_word():
    text = format_analysis(
        {
            "surah": 1,
            "ayah": 2,
            "accuracy_pct": 75.0,
            "expected_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
            "word_alignment": [
                {"expected": "الحمد", "heard": "الحمد", "status": "correct"},
                {"expected": "لله", "heard": "لله", "status": "correct"},
                {"expected": "رب", "heard": "رب", "status": "correct"},
                {
                    "expected": "العالمين",
                    "heard": "العالمون",
                    "status": "incorrect",
                },
            ],
        }
    )

    assert "75.0%" in text
    assert "العالمين" in text
    assert "العالمون" in text
    assert "tahsin" not in text.lower()
