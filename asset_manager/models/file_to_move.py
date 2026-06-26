from pathlib import Path
from dataclasses import dataclass


@dataclass
class FileToMove:
    source: Path
    destination: Path
