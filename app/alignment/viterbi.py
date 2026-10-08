from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


class CTCAlignmentError(RuntimeError):
    pass


@dataclass(frozen=True)
class TokenSegment:
    token_index: int
    token_id: int
    start_frame: int
    end_frame: int
    confidence: float


@dataclass(frozen=True)
class CTCAlignment:
    path_score: float
    token_segments: tuple[TokenSegment, ...]


def _value(log_probs, frame: int, token_id: int) -> float:
    try:
        return float(log_probs[frame][token_id])
    except (IndexError, TypeError) as exc:
        raise CTCAlignmentError(
            f"Invalid log-probability matrix access frame={frame}, token={token_id}"
        ) from exc


def ctc_viterbi_align(
    log_probs: Sequence[Sequence[float]],
    token_ids: Sequence[int],
    blank_id: int,
) -> CTCAlignment:
    """Align a fixed CTC token sequence to frame-level log probabilities.

    Uses the standard blank-interleaved CTC state graph. Repeated adjacent
    tokens must pass through a blank state before the second token.
    """
    frame_count = len(log_probs)
    if frame_count == 0:
        raise CTCAlignmentError("No CTC frames were provided")
    if not token_ids:
        return CTCAlignment(path_score=0.0, token_segments=())

    expanded: list[int] = [blank_id]
    for token_id in token_ids:
        expanded.extend((int(token_id), blank_id))

    state_count = len(expanded)
    neg_inf = -math.inf

    previous = [neg_inf] * state_count
    backpointers = [[-1] * state_count for _ in range(frame_count)]

    previous[0] = _value(log_probs, 0, blank_id)
    backpointers[0][0] = 0
    if state_count > 1:
        previous[1] = _value(log_probs, 0, expanded[1])
        backpointers[0][1] = 1

    for frame in range(1, frame_count):
        current = [neg_inf] * state_count

        for state, label in enumerate(expanded):
            candidates: list[tuple[float, int]] = [(previous[state], state)]

            if state > 0:
                candidates.append((previous[state - 1], state - 1))

            if (
                state > 1
                and label != blank_id
                and label != expanded[state - 2]
            ):
                candidates.append((previous[state - 2], state - 2))

            best_score, best_previous_state = max(
                candidates,
                key=lambda candidate: candidate[0],
            )
            if math.isfinite(best_score):
                current[state] = best_score + _value(
                    log_probs,
                    frame,
                    label,
                )
                backpointers[frame][state] = best_previous_state

        previous = current

    final_states = [state_count - 1]
    if state_count > 1:
        final_states.append(state_count - 2)

    final_state = max(final_states, key=lambda state: previous[state])
    final_score = previous[final_state]
    if not math.isfinite(final_score):
        raise CTCAlignmentError(
            "No valid CTC path exists for the requested token sequence"
        )

    states = [0] * frame_count
    states[-1] = final_state
    for frame in range(frame_count - 1, 0, -1):
        prior = backpointers[frame][states[frame]]
        if prior < 0:
            raise CTCAlignmentError("CTC backtracking encountered an invalid state")
        states[frame - 1] = prior

    segments: list[TokenSegment] = []
    for token_index, token_id in enumerate(token_ids):
        token_state = 2 * token_index + 1
        token_frames = [
            frame
            for frame, state in enumerate(states)
            if state == token_state
        ]
        if not token_frames:
            raise CTCAlignmentError(
                f"Token index {token_index} received no aligned frames"
            )

        start = token_frames[0]
        end = token_frames[-1] + 1
        confidence = sum(
            math.exp(_value(log_probs, frame, int(token_id)))
            for frame in token_frames
        ) / len(token_frames)

        segments.append(
            TokenSegment(
                token_index=token_index,
                token_id=int(token_id),
                start_frame=start,
                end_frame=end,
                confidence=round(float(confidence), 6),
            )
        )

    return CTCAlignment(
        path_score=float(final_score),
        token_segments=tuple(segments),
    )
