from typing import Optional

import click
from dotenv import load_dotenv
from pynput import keyboard


from asset_manager.models.config import Config
from asset_manager.models.file_to_move import FileToMove
from asset_manager.services.asset_service import AssetService
from asset_manager.services.excel_reader import ExcelReader
from asset_manager.utils.sanitize_input import sanitize_input
from asset_manager.utils.build_destination_path import build_destination_path

class CLIApp:
    _config: Optional[Config] = None
    _KEYS_TO_RELOAD = ["R", "r"]

    def _load_environment(self):
        load_dotenv(override=True)
        self._config = sanitize_input()

        click.secho("Environment variables are loaded successfully", fg='green', bold=True)

    def _handle_key_press(self, key: str):
        try:
            if key.char in self._KEYS_TO_RELOAD:
                self._load_environment()
        except AttributeError:
            pass

    def _move_assets(self, data):
        asset_service = AssetService(self._config.source_files_folder)
        source_file_paths = asset_service.find_source_paths(glob=self._config.glob)

        source_files_paths_count = len(source_file_paths)

        if source_files_paths_count:
            all_sources_files = "\n".join(path.stem for path in source_file_paths)

            click.confirm(
                text=f"Found {source_files_paths_count} files:\n{all_sources_files}\n",
                abort=True
            )

            files_to_move = []

            for source_path in source_file_paths:
                destination_path = build_destination_path(
                    source_file_path=source_path,
                    data=data,
                    destination_folder=self._config.destination_folder,
                    document_type=self._config.document_type,
                )

                if destination_path:
                    file_to_move = FileToMove(source=source_path, destination=destination_path)
                    files_to_move.append(file_to_move)

            all_operations = '\n'.join(
                f"Source: {file.source}, destination: {file.destination}" for file in files_to_move
            )

            click.confirm(
                text=f"Move {len(files_to_move)} files?\nFiles to move:\n{all_operations}\n",
                abort=True,
            )

            # TODO: implement atomiticity of operations
            for file in files_to_move:
                asset_service.move_file(source=file.source, destination=file.destination)

            click.secho(f"Successfully processed {len(files_to_move)} files", fg='green', bold=True)

    def run(self):
        listener = None

        try:
            click.secho("Starting app", fg='green', bold=True)

            self._load_environment()

            excel_reader = ExcelReader(
                workbook_path=self._config.excel_workbook_path,
                table_name=self._config.excel_table_name,
                worksheet_name=self._config.excel_worksheet_name,
                remove_last_row=True,
            )
            data = excel_reader.run()

            listener = keyboard.Listener(on_press=self._handle_key_press)
            listener.start()

            click.secho("App started", fg='green', bold=True)
            click.echo("-> Press [R] for reload .env config")
            click.echo("-> Press [Ctrl+C] for exit\n")

            while True:
                self._move_assets(data=data)
        except KeyboardInterrupt:
            click.secho("\nFinished app work!", fg='red', bold=True)
        except Exception as error:
            click.secho(f"\nUnexpected error happened!: {error}", fg='red', bold=True)
        finally:
            if listener:
                listener.stop()

@click.command
def launch_app():
    app = CLIApp()
    app.run()