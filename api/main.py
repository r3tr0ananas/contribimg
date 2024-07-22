from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse, JSONResponse
from fastapi.requests import Request
import os

from . import __version__
from .http_client import HTTPClient
from .image import IMG

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH"))

http = HTTPClient()
img = IMG()

app = FastAPI(
    title = "contribimg", 
    description = "", 
    license_info = {
        "name": "MIT", 
        "identifier": "MIT",
    }, 
    version = f"v{__version__}",

    root_path = ROOT_PATH
)

@app.get("/")
async def root():
    return RedirectResponse(f"{ROOT_PATH}/docs")

@app.get("/{owner}/{repo}")
async def owner_repo(
    request: Request, 
    owner: str,
    repo: str,
) -> StreamingResponse: 
    id = f"{owner}/{repo}"
    cache = img.get_cache(id)

    if cache is not None:
        return StreamingResponse(
            cache,
            headers  = {
                "Content-Type": "image/webp",
                "Expires": "86400"
            }
        )

    images = await http.contributor_images(owner, repo)

    if isinstance(images, int):
        return JSONResponse(
            {
                "status": int,
                "message": "Something went wrong"
            },
            images
        )

    image = img.make(id, images)

    return StreamingResponse(
        image,
        headers = {
            "Content-Type": "image/webp",
            "Expires": "86400"
        }
    )