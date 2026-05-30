from dataclasses import dataclass
from pathlib import Path


@dataclass
class AssetsMoveInput:
    excel_workbook_path: Path
    source_files_folder: Path
    destination_folder: Path
    glob: str
    document_type: str
