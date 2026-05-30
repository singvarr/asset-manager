# Asset manager

A simple python app that finds assets by pattern and moves them to target directories.

## Running of application

1. Install dependencies `pip install - r requirements.txt`
2. Create `.env` file (see [template](./env-template))
3. Create module `asset_manager.utils.build_destination_path`. This module should contain function `build_destination_path` that accepts source path (`Path` from `pathlib`) and returns `None` or destination path (also `Path` from `pathlib`). This function maps source file name and destination path; implement it according to your naming convention. Use [service for reading data from excel table](./asset_manager/services/excel_reader.py) if needed.
4. Launch application using `python -m asset_manager.main`
