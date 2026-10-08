from app.phonetics.alignment import analyze_phonemes


def test_phoneme_substitution_is_explicit():
    result = analyze_phonemes(
        ["ħ", "a", "m", "d"],
        ["h", "a", "m", "d"],
    )

    assert result["counts"]["substitution"] == 1
    assert result["counts"]["correct"] == 3
    assert result["alignment"][0] == {
        "expected": "ħ",
        "observed": "h",
        "status": "substitution",
    }


def test_phoneme_deletion_is_explicit():
    result = analyze_phonemes(
        ["ʕ", "a:", "l"],
        ["ʕ", "l"],
    )

    assert result["counts"]["deletion"] == 1
    assert result["counts"]["substitution"] == 0
