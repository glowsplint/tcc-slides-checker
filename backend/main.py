import os
import time
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.file_io import get_output_path
from backend.metadata import metadata

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE")
app = FastAPI(**metadata)

EXPORTED_PATH = Path("./frontend/out/")
app.mount("/_next", StaticFiles(directory=EXPORTED_PATH / "_next"))
app.mount("/static", StaticFiles(directory=EXPORTED_PATH))


def set_appropriate_middleware(mode: bool) -> None:
    """
    Adds CORS middleware if DEVELOPMENT_MODE is set to True.
    """
    if mode:
        origins = [
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5000",
            "http://localhost:3000",
            "http://localhost:5000",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


set_appropriate_middleware(mode=(DEVELOPMENT_MODE == "True"))


@app.get("/")
async def root_page() -> FileResponse:
    """
    Serves the front-end static HTML file.
    Returns:
        FileResponse: The exported static `index.html` file.
    """
    return FileResponse(EXPORTED_PATH / "index.html")


@app.post("/api/upload/")
async def upload_handler(
    selected_date: str = Form(...),
    req_order_of_service: str = Form(...),
    sermon_discussion_qns: str = Form(...),
    files: list[UploadFile] = File(...),
) -> dict:
    """
    Primary endpoint which handles the POST request.
    Args:
        files (list[UploadFile], optional): User-uploaded input files. Defaults to File(...).
    Returns:
        FileResponse: Excel spreadsheet output
    """
    time.sleep(5)
    return {"message": "morp"}
