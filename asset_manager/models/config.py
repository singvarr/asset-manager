from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    excel_workbook_path: Path
    source_files_folder: Path
    destination_folder: Path
    glob: str
    document_type: str
    excel_worksheet_name: str
    excel_table_name: str
