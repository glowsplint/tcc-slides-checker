from pathlib import Path
from shutil import rmtree

from fastapi import UploadFile


def get_output_path(files: list[UploadFile]) -> Path:
    """
    Generates the output file and returns the file path.
    Args:
        files (list[UploadFile]): User-uploaded input files
    Returns:
        Path: Output file path
    """

    return


def clean_up_outputs(path: Path):
    """
    Deletes the specified path recursively.
    Args:
        path (Path): Specified path
    """
    rmtree(path, ignore_errors=True)
