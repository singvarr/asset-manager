import os
import shutil
from pathlib import Path


class AssetService:
    def __init__(self, source_files_folder: Path):
        self._source_files_folder = source_files_folder

    def find_source_paths(self, glob: str) -> list[Path]:
        return list(self._source_files_folder.rglob(glob))

    def move_file(self, source: Path, destination: Path):
        dest_dir = os.path.dirname(destination)

        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        shutil.move(source, destination)
