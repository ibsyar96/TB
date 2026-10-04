from abc import ABC, abstractmethod
from pathlib import Path


class ASRProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path) -> str:
        raise NotImplementedError
