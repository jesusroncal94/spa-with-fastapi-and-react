from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

API_PREFIX = "api/"


def mount_single_page_app(app: FastAPI, directory: Path) -> None:
    app.mount("/assets", StaticFiles(directory=directory / "assets"), name="assets")
    index = directory / "index.html"

    @app.get("/{requested_path:path}", include_in_schema=False)
    async def serve_app(requested_path: str) -> FileResponse:
        if requested_path.startswith(API_PREFIX):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        candidate = directory / requested_path
        if requested_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(index)
