from app.phonetics.reference import expected_pronunciation


def test_quranic_phonemizer_returns_hafs_reference():
    result = expected_pronunciation(1, 4)

    assert result["reference"] == "1:4"
    assert result["text"]
    assert len(result["phonemes"]) > 5
    assert all(isinstance(token, str) for token in result["phonemes"])
    assert isinstance(result["rule_ids"], list)
