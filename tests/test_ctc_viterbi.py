import math

import pytest

from app.alignment.viterbi import CTCAlignmentError, ctc_viterbi_align


def _log_rows(prob_rows):
    return [[math.log(value) for value in row] for row in prob_rows]


def test_ctc_viterbi_aligns_two_tokens_with_blanks():
    # vocab: 0=blank, 1=A, 2=B
    log_probs = _log_rows([
        [0.90, 0.05, 0.05],
        [0.05, 0.90, 0.05],
        [0.90, 0.05, 0.05],
        [0.05, 0.05, 0.90],
        [0.90, 0.05, 0.05],
    ])

    result = ctc_viterbi_align(log_probs, [1, 2], blank_id=0)

    assert [(s.start_frame, s.end_frame) for s in result.token_segments] == [
        (1, 2),
        (3, 4),
    ]
    assert result.token_segments[0].confidence == pytest.approx(0.9)
    assert result.token_segments[1].confidence == pytest.approx(0.9)


def test_ctc_viterbi_requires_blank_between_repeated_tokens():
    log_probs = _log_rows([
        [0.90, 0.10],
        [0.10, 0.90],
        [0.90, 0.10],
        [0.10, 0.90],
        [0.90, 0.10],
    ])

    result = ctc_viterbi_align(log_probs, [1, 1], blank_id=0)

    assert [(s.start_frame, s.end_frame) for s in result.token_segments] == [
        (1, 2),
        (3, 4),
    ]


def test_ctc_viterbi_rejects_impossible_repeated_sequence():
    log_probs = _log_rows([
        [0.50, 0.50],
        [0.50, 0.50],
    ])

    with pytest.raises(CTCAlignmentError):
        ctc_viterbi_align(log_probs, [1, 1], blank_id=0)
