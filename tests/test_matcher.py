from app.quran.data import get_ayah
from app.tahsin.matcher import analyze_text


def test_exact_recitation_is_100_percent():
    expected = get_ayah(1, 2)
    result = analyze_text(expected, "الحمد لله رب العالمين")

    assert result["accuracy_pct"] == 100.0
    assert result["counts"]["correct"] == 4


def test_missing_word_is_detected():
    expected = get_ayah(1, 2)
    result = analyze_text(expected, "الحمد لله العالمين")

    assert result["counts"]["missed"] == 1
    assert any(
        item["expected"] == "رب" and item["status"] == "missed"
        for item in result["word_alignment"]
    )


def test_replacement_is_incorrect_not_double_counted():
    expected = get_ayah(1, 2)
    result = analyze_text(expected, "الحمد لله رب العالمون")

    assert result["counts"]["incorrect"] == 1
    assert result["counts"]["extra"] == 0
    assert result["counts"]["missed"] == 0
