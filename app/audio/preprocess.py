import shutil
import subprocess
from pathlib import Path


class AudioPreprocessError(RuntimeError):
    pass


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def build_ffmpeg_command(input_path: Path, output_path: Path) -> list[str]:
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]


def normalize_audio(input_path: Path, output_path: Path) -> Path:
    """Convert arbitrary voice/audio input to mono 16 kHz PCM WAV."""
    if not ffmpeg_available():
        raise AudioPreprocessError(
            "ffmpeg is not installed. The ASR worker requires ffmpeg."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_ffmpeg_command(input_path, output_path)
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "ffmpeg failed to normalize audio"
        raise AudioPreprocessError(message)

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise AudioPreprocessError("ffmpeg produced an empty audio file")

    return output_path
