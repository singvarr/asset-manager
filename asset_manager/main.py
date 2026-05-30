from logging import getLogger, DEBUG

from dotenv import load_dotenv
import click

from asset_manager.models.file_to_move import FileToMove
from asset_manager.services.asset_service import AssetService
from asset_manager.services.excel_reader import ExcelReader
from asset_manager.utils.sanitize_input import sanitize_input
from asset_manager.utils.build_destination_path import build_destination_path

logger = getLogger("Assets manager")
logger.setLevel(DEBUG)


if __name__ == "__main__":
    try:
        load_dotenv()

        sanitized_input = sanitize_input()

        asset_service = AssetService(sanitized_input.source_files_folder)
        source_file_paths = asset_service.find_source_paths(glob=sanitized_input.glob)

        source_files_paths_count = len(source_file_paths)

        if source_files_paths_count:
            all_sources_files = "\n".join(path.stem for path in source_file_paths)
            click.confirm(
                text=f"Found {source_files_paths_count} files:\n{all_sources_files}\n",
                abort=True
            )

            excel_reader = ExcelReader(
                workbook_path=sanitized_input.excel_workbook_path,
                table_name=sanitized_input.excel_table_name,
                worksheet_name=sanitized_input.excel_worksheet_name,
                remove_last_row=True,
            )
            data = excel_reader.run()

            files_to_move = []

            for source_path in source_file_paths:
                destination_path = build_destination_path(
                    source_file_path=source_path,
                    data=data,
                    destination_folder=sanitized_input.destination_folder,
                    document_type=sanitized_input.document_type,
                )

                if destination_path:
                    file_to_move = FileToMove(source=source_path, destination=destination_path)
                    files_to_move.append(file_to_move)
                else:
                    logger.warning(f'No destination found for {source_path}')

            all_operations = '\n'.join(
                f"Source: {file.source}, destination: {file.destination}" for file in files_to_move
            )
            click.confirm(text=f"Files to move:\n{all_operations}\n", abort=True)

            for file in files_to_move:
                # TODO: implement atomiticity of operations
                asset_service.move_file(source=file.source, destination=file.destination)
        else:
            logger.info(f"No files matched glob {sanitized_input.glob}")
    except Exception as error:
        logger.error(f"Failed to move assets with error {error}")
