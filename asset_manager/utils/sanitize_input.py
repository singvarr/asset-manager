import os
from pathlib import Path

from asset_manager.models.config import Config
from asset_manager.utils.check_required_env_variables import (
    check_required_env_variables,
)

REQUIRED_ENV_VARIABLES = (
    "SOURCE_FILES_GLOB",
    "SOURCE_FILES_FOLDER_PATH",
    "EXCEL_WORKBOOK_PATH",
    "DESTINATION_PATH",
    "DOCUMENT_TYPE",
    "EXCEL_TABLE_NAME",
    "EXCEL_WORKSHEET_NAME",
)


def sanitize_input() -> Config:
    check_required_env_variables(required_env_variables=REQUIRED_ENV_VARIABLES)

    return Config(
        excel_workbook_path=Path(os.environ["EXCEL_WORKBOOK_PATH"]),
        glob=os.environ["SOURCE_FILES_GLOB"],
        source_files_folder=Path(os.environ["SOURCE_FILES_FOLDER_PATH"]),
        destination_folder=Path(os.environ["DESTINATION_PATH"]),
        document_type=os.environ["DOCUMENT_TYPE"],
        excel_table_name=os.environ["EXCEL_TABLE_NAME"],
        excel_worksheet_name=os.environ["EXCEL_WORKSHEET_NAME"],
    )
