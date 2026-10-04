from pathlib import Path

from app.audio.preprocess import build_ffmpeg_command


def test_ffmpeg_command_normalizes_for_quran_asr():
    command = build_ffmpeg_command(
        Path("voice.ogg"),
        Path("normalized.wav"),
    )

    assert "-ac" in command
    assert command[command.index("-ac") + 1] == "1"
    assert "-ar" in command
    assert command[command.index("-ar") + 1] == "16000"
    assert "pcm_s16le" in command
