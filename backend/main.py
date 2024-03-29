import io
import os
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pptx import Presentation

from backend.metadata import metadata
from backend.processing.checker.content import MultiContentChecker
from backend.processing.result import FileResults

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
) -> list[FileResults]:
    """
    Primary endpoint which handles the POST request.

    Args:
        files (list[UploadFile], optional): User-uploaded input files. Defaults to File(...).

    Returns:
        dict: JSON response containing the test results
    """
    presentations = dict()
    for file in files:
        with file.file as f:
            bytes_io = io.BytesIO(f.read())
            presentations[file.filename] = Presentation(pptx=bytes_io)

    mcc = MultiContentChecker(
        selected_date=selected_date,
        req_order_of_service=req_order_of_service,
        sermon_discussion_qns=sermon_discussion_qns,
        presentations=presentations,
    )
    return mcc.run()
