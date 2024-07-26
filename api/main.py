from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, StreamingResponse, JSONResponse, Response
from fastapi.requests import Request

from .image import IMG
from . import __version__
from .http_client import HTTPClient


ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH"))

img = IMG()
http = HTTPClient()

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
                "status": images, 
                "message": "Something went wrong"
            },
            images
        )

    image_bytes = img.make(id, images)

    return Response(
        image_bytes, 
        headers = {
            "Content-Type": "image/webp",
            # "Expires": "86400"
        }
    )