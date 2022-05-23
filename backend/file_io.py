from pathlib import Path

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
