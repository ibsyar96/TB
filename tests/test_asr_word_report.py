from app.services.recitation import analyze_transcription
from app.telegram.formatting import format_analysis


def test_asr_transcription_does_not_claim_kaf_is_heard():
    analysis = analyze_transcription(
        surah=1,
        ayah=2,
        transcription="الحمد لله رب الكالمين",
        asr_mode="remote-worker",
    )
    reply = format_analysis(analysis)

    assert analysis["accuracy_pct"] == 75.0
    assert "Padanan perkataan dalam transkrip" in reply
    assert "Transkrip mentah AI (mungkin tersalah dengar)" in reply
    assert "الكالمين" in reply
    assert "belum dapat dipastikan" in reply
    assert "bukan markah bacaan, tajwid atau makhraj" in reply
    assert "dikesan <b>الكالمين</b>" not in reply


def test_asr_perfect_text_does_not_claim_tajwid_or_makhraj_perfect():
    analysis = analyze_transcription(
        1, 2, "الحمد لله رب العالمين", asr_mode="remote-worker"
    )
    reply = format_analysis(analysis)
    assert "Semua perkataan sepadan dalam transkrip AI" in reply
    assert "bukan markah bacaan, tajwid atau makhraj" in reply


def test_asr_missed_word_does_not_claim_reader_skipped_it():
    analysis = analyze_transcription(
        1, 2, "الحمد لله العالمين", asr_mode="remote-worker"
    )
    reply = format_analysis(analysis)
    assert "belum tentu ditinggalkan ketika membaca" in reply
    assert "tertinggal" not in reply


def test_manual_transcript_still_reports_only_literal_text_difference():
    analysis = analyze_transcription(
        1, 2, "الحمد لله رب العالمون"
    )
    reply = format_analysis(analysis)
    assert "Padanan perkataan teks" in reply
    assert "teks diberi" in reply
    assert "Transkrip mentah AI" not in reply


def test_html_escape_untrusted_asr_text():
    analysis = {
        "surah": 1,
        "ayah": 2,
        "asr_mode": "remote-worker",
        "accuracy_pct": 0,
        "word_alignment": [
            {"expected": "العالمين", "heard": "<tag>", "status": "incorrect"}
        ],
        "expected_text": "العالمين",
        "transcription": "<tag>&",
    }
    reply = format_analysis(analysis)
    assert "<tag>" not in reply
    assert "&lt;tag&gt;&amp;" in reply
